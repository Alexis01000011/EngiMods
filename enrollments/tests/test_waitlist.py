import csv
import io
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.urls import reverse
from django.utils import timezone

from accounts.models import PrivacyConsent
from catalog.models import Game
from core.models import LegalText
from courses.models import Course
from enrollments.models import WaitlistEntry

pytestmark = pytest.mark.django_db

WAITLIST_URL = reverse("waitlist:join")


@pytest.fixture
def aviso():
    return LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="1.0",
        body="Texto del aviso.",
        effective_date=timezone.localdate() - timedelta(days=1),
    )


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego para probar la lista de espera.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def otro_juego():
    return Game.objects.create(
        name="Otro juego",
        slug="otro-juego",
        description="Otro juego de prueba.",
        official_url="https://example.org/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def course(game):
    return Course.objects.create(
        title="Curso de prueba",
        slug="curso-de-prueba",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Un curso para probar la lista de espera.",
        requirements="Computadora y el juego.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )


@pytest.fixture
def otro_course(otro_juego):
    return Course.objects.create(
        title="Curso de otro juego",
        slug="curso-de-otro-juego",
        game=otro_juego,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Un curso de otro juego.",
        requirements="Computadora y el juego.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )


def datos(**cambios):
    return {
        "email": "interesada@example.com",
        "game": "",
        "course": "",
        "accept_privacy": "on",
        **cambios,
    }


def test_la_url_publica_esta_en_espanol():
    assert WAITLIST_URL == "/lista-de-espera/"


def test_el_formulario_pide_correo_juego_o_curso_y_aviso(client, aviso, game, course):
    response = client.get(WAITLIST_URL)
    assert response.status_code == 200
    html = response.content.decode()
    for name in ("email", "game", "course", "accept_privacy"):
        assert f'name="{name}"' in html
    assert 'type="email"' in html
    assert "versión 1.0" in html
    assert game.name in html
    assert course.title in html


def test_deja_el_correo_y_guarda_el_consentimiento_sin_cuenta(client, aviso, game):
    response = client.post(WAITLIST_URL, datos(game=game.pk))
    assert response.status_code == 302
    assert response.url == WAITLIST_URL

    entry = WaitlistEntry.objects.get()
    assert entry.email == "interesada@example.com"
    assert entry.game == game
    assert entry.course is None
    assert entry.legal_text == aviso

    consent = PrivacyConsent.objects.get()
    assert consent.user is None
    assert consent.email == entry.email
    assert consent.legal_text == aviso

    assert not get_user_model().objects.exists()
    assert "_auth_user_id" not in client.session
    assert len(mail.outbox) == 0


def test_si_elige_un_curso_no_hace_falta_repetir_el_juego(client, aviso, course):
    response = client.post(WAITLIST_URL, datos(course=course.pk))
    assert response.status_code == 302
    entry = WaitlistEntry.objects.get()
    assert entry.course == course
    assert entry.game == course.game


def test_avisa_si_el_curso_no_es_del_juego_elegido(client, aviso, game, otro_course):
    response = client.post(WAITLIST_URL, datos(game=game.pk, course=otro_course.pk))
    assert response.status_code == 200
    assert not WaitlistEntry.objects.exists()
    assert "no es de ese juego" in response.content.decode()


def test_pide_elegir_al_menos_un_juego_o_curso(client, aviso):
    response = client.post(WAITLIST_URL, datos())
    assert response.status_code == 200
    assert not WaitlistEntry.objects.exists()
    assert "Elige un juego o un curso" in response.content.decode()


def test_sin_aceptar_el_aviso_no_guarda_nada(client, aviso, game):
    response = client.post(WAITLIST_URL, datos(game=game.pk, accept_privacy=""))
    assert response.status_code == 200
    assert not WaitlistEntry.objects.exists()
    assert not PrivacyConsent.objects.exists()
    assert "acepta el aviso de privacidad" in response.content.decode()


def test_un_correo_incompleto_dice_como_escribirlo(client, aviso, game):
    response = client.post(WAITLIST_URL, datos(email="interesada@", game=game.pk))
    assert response.status_code == 200
    assert not WaitlistEntry.objects.exists()
    assert "nombre@dominio.mx" in response.content.decode()


def test_solo_ofrece_juegos_activos_y_cursos_publicados(
    client, aviso, game, course, otro_juego, otro_course
):
    oculto = Game.objects.create(
        name="Juego oculto",
        slug="juego-oculto",
        description="No debe aparecer.",
        official_url="https://example.net/",
        status=Game.Status.HIDDEN,
    )
    borrador = Course.objects.create(
        title="Curso en borrador",
        slug="curso-en-borrador",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Todavía no se publica.",
        requirements="Computadora.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.DRAFT,
    )
    Course.objects.create(
        title="Curso de juego oculto",
        slug="curso-de-juego-oculto",
        game=oculto,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Su juego no es público.",
        requirements="Computadora.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )

    html = client.get(WAITLIST_URL).content.decode()
    assert game.name in html
    assert course.title in html
    assert otro_juego.name in html
    assert otro_course.title in html
    assert "Juego oculto" not in html
    assert "Curso en borrador" not in html
    assert "Curso de juego oculto" not in html

    assert client.post(WAITLIST_URL, datos(game=oculto.pk)).status_code == 200
    assert client.post(WAITLIST_URL, datos(course=borrador.pk)).status_code == 200
    assert (
        client.post(
            WAITLIST_URL,
            datos(game=game.pk, course=Course.objects.get(slug="curso-de-juego-oculto").pk),
        ).status_code
        == 200
    )
    assert not WaitlistEntry.objects.exists()


def test_sin_aviso_vigente_no_muestra_formulario_ni_guarda_nada(client, game):
    response = client.get(WAITLIST_URL)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Todavía no abrimos la lista de espera" in html
    assert 'name="email"' not in html

    response = client.post(WAITLIST_URL, datos(game=game.pk))
    assert response.status_code == 200
    assert not WaitlistEntry.objects.exists()
    assert not PrivacyConsent.objects.exists()


def test_guarda_la_version_vigente_del_aviso(client, game):
    anterior = LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="1.0",
        body="Aviso anterior.",
        effective_date=timezone.localdate() - timedelta(days=30),
    )
    vigente = LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="1.1",
        body="Aviso vigente.",
        effective_date=timezone.localdate(),
    )
    client.post(WAITLIST_URL, datos(game=game.pk))
    entry = WaitlistEntry.objects.get()
    assert entry.legal_text == vigente
    assert entry.legal_text != anterior
    assert PrivacyConsent.objects.get().legal_text == vigente


def test_el_modelo_rechaza_un_curso_de_otro_juego(aviso, game, otro_course):
    entry = WaitlistEntry(
        email="interesada@example.com", game=game, course=otro_course, legal_text=aviso
    )
    with pytest.raises(ValidationError) as error:
        entry.full_clean()
    assert "course" in error.value.message_dict


def test_el_modelo_rechaza_un_texto_legal_que_no_es_de_privacidad(game):
    terminos = LegalText.objects.create(
        kind=LegalText.Kind.TERMS,
        version="1.0",
        body="Términos.",
        effective_date=timezone.localdate(),
    )
    entry = WaitlistEntry(email="interesada@example.com", game=game, legal_text=terminos)
    with pytest.raises(ValidationError) as error:
        entry.full_clean()
    assert "legal_text" in error.value.message_dict


def test_no_se_borra_el_juego_de_la_lista_de_espera(aviso, game):
    WaitlistEntry.objects.create(email="interesada@example.com", game=game, legal_text=aviso)
    with pytest.raises(ProtectedError):
        game.delete()


def test_no_se_borra_el_curso_de_la_lista_de_espera(aviso, course):
    WaitlistEntry.objects.create(
        email="interesada@example.com", game=course.game, course=course, legal_text=aviso
    )
    with pytest.raises(ProtectedError):
        course.delete()


def test_no_se_borra_el_aviso_aceptado_por_la_lista_de_espera(aviso, game):
    WaitlistEntry.objects.create(email="interesada@example.com", game=game, legal_text=aviso)
    with pytest.raises(ProtectedError):
        aviso.delete()


def test_el_admin_ve_la_lista_y_no_la_puede_editar(admin_client, aviso, game):
    WaitlistEntry.objects.create(email="interesada@example.com", game=game, legal_text=aviso)
    response = admin_client.get(reverse("admin:enrollments_waitlistentry_changelist"))
    assert response.status_code == 200
    assert "interesada@example.com" in response.content.decode()
    assert admin_client.get(reverse("admin:enrollments_waitlistentry_add")).status_code == 403


def test_el_admin_ve_la_lista_agrupada_por_juego(admin_client, aviso, game, otro_juego):
    WaitlistEntry.objects.create(email="uno@example.com", game=otro_juego, legal_text=aviso)
    WaitlistEntry.objects.create(email="dos@example.com", game=game, legal_text=aviso)
    response = admin_client.get(reverse("admin:enrollments_waitlistentry_grouped"))
    assert response.status_code == 200
    html = response.content.decode()
    assert "uno@example.com" in html
    assert "dos@example.com" in html
    assert html.index(game.name) < html.index(otro_juego.name)


def test_el_admin_exporta_la_lista_en_csv_ordenada_por_juego(
    admin_client, aviso, game, otro_juego, course
):
    WaitlistEntry.objects.create(email="dos@example.com", game=otro_juego, legal_text=aviso)
    WaitlistEntry.objects.create(
        email="uno@example.com", game=game, course=course, legal_text=aviso
    )
    response = admin_client.get(reverse("admin:enrollments_waitlistentry_export"))
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert "lista-de-espera.csv" in response["Content-Disposition"]

    rows = list(csv.reader(io.StringIO(response.content.decode())))
    assert rows[0] == [
        "Juego",
        "Curso",
        "Correo",
        "Aviso de privacidad",
        "Registrado el",
    ]
    assert [row[0] for row in rows[1:]] == [game.name, otro_juego.name]
    assert rows[1][1] == course.title
    assert rows[1][2] == "uno@example.com"


def test_el_csv_no_interpreta_nombres_como_formulas(admin_client, aviso):
    game = Game.objects.create(
        name="=2+2",
        slug="juego-formula",
        description="Prueba.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )
    course = Course.objects.create(
        title="@SUMA",
        slug="curso-formula",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Prueba.",
        requirements="Computadora.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )
    WaitlistEntry.objects.create(
        email="interesada@example.com", game=game, course=course, legal_text=aviso
    )
    response = admin_client.get(reverse("admin:enrollments_waitlistentry_export"))
    fila = list(csv.reader(io.StringIO(response.content.decode())))[1]
    assert fila[0] == "'=2+2"
    assert fila[1] == "'@SUMA"


def test_la_exportacion_requiere_permiso_de_ver_la_lista(client, aviso, game):
    WaitlistEntry.objects.create(email="interesada@example.com", game=game, legal_text=aviso)
    staff = get_user_model().objects.create_user(
        email="staff@example.com", password="x-12345678", display_name="Staff", is_staff=True
    )
    client.force_login(staff)
    for name in (
        "admin:enrollments_waitlistentry_export",
        "admin:enrollments_waitlistentry_grouped",
    ):
        assert client.get(reverse(name)).status_code == 403


def test_un_visitante_no_entra_a_la_exportacion(client):
    response = client.get(reverse("admin:enrollments_waitlistentry_export"))
    assert response.status_code == 302
    assert "/admin/login/" in response.url


def test_el_enlace_de_un_juego_preselecciona_ese_juego(client, aviso, game, otro_juego):
    content = client.get(WAITLIST_URL, {"juego": game.slug}).content.decode()
    assert f'<option value="{game.pk}" selected>' in content
    assert f'<option value="{otro_juego.pk}">' in content


def test_un_juego_oculto_o_inexistente_no_se_preselecciona(client, aviso, game):
    game.status = Game.Status.HIDDEN
    game.save()
    for slug in (game.slug, "no-existe"):
        content = client.get(WAITLIST_URL, {"juego": slug}).content.decode()
        assert f'<option value="{game.pk}" selected>' not in content
