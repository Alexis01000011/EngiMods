"""Guía de laboratorio por juego (EM-063)."""

from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, LabGuide, LabStep, ModdingEnvironment
from courses.models import Course
from enrollments.models import Enrollment, LabStepProgress

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def version(game):
    return GameVersion.objects.create(
        game=game, number="1.4", release_date=date(2026, 1, 1), is_current=True
    )


@pytest.fixture
def environment(game, version):
    environment = ModdingEnvironment.objects.create(game=game, name="Loader", version="2.1")
    environment.compatible_versions.add(version)
    return environment


@pytest.fixture
def guide(game, version, environment):
    return LabGuide.objects.create(
        game=game,
        game_version=version,
        modding_environment=environment,
        requirements="Computadora con el juego instalado.",
        final_check="Abre el juego con el entorno cargado.",
    )


@pytest.fixture
def steps(guide):
    first = LabStep.objects.create(
        guide=guide, order=1, title="Instala el juego", instructions="Descarga e instala."
    )
    second = LabStep.objects.create(
        guide=guide, order=2, title="Instala el entorno", instructions="Copia el loader."
    )
    return first, second


@pytest.fixture
def course(game):
    return Course.objects.create(
        title="Curso de prueba",
        slug="curso-de-prueba",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )


def make_user(email, **extra):
    return get_user_model().objects.create_user(
        email=email, password="x-12345678", display_name=email.split("@")[0], **extra
    )


def enrol(user, course, **extra):
    return Enrollment.objects.create(
        user=user, course=course, origin=Enrollment.Origin.SCHOLARSHIP, **extra
    )


def guide_url(guide):
    return reverse("enrollments:lab_guide", args=[guide.game.slug])


def toggle_url(step):
    return reverse("enrollments:toggle_lab_step", args=[step.guide.game.slug, step.pk])


def test_no_acepta_version_de_otro_juego(guide, environment):
    other_game = Game.objects.create(
        name="Otro", slug="otro", description="Otro.", official_url="https://example.com/"
    )
    other_version = GameVersion.objects.create(
        game=other_game, number="9.9", release_date=date(2026, 1, 1)
    )
    guide.game_version = other_version

    with pytest.raises(ValidationError) as error:
        guide.full_clean()

    assert "game_version" in error.value.message_dict


def test_no_acepta_entorno_de_otro_juego(guide, version):
    other_game = Game.objects.create(
        name="Otro", slug="otro", description="Otro.", official_url="https://example.com/"
    )
    other_environment = ModdingEnvironment.objects.create(
        game=other_game, name="Otro loader", version="1.0"
    )
    guide.modding_environment = other_environment

    with pytest.raises(ValidationError) as error:
        guide.full_clean()

    assert "modding_environment" in error.value.message_dict


def test_sin_sesion_redirige_al_inicio(client, guide, steps):
    response = client.get(guide_url(guide))

    assert response.status_code == 302
    assert response.url.startswith(reverse("accounts:login"))


def test_alumno_inscrito_ve_la_guia(client, guide, steps, course):
    user = make_user("alumno@example.com")
    enrol(user, course)
    client.force_login(user)

    html = client.get(guide_url(guide)).content.decode()

    assert "Juego de prueba" in html
    assert "Computadora con el juego instalado." in html
    assert "Instala el juego" in html
    assert "Instala el entorno" in html
    assert "Abre el juego con el entorno cargado." in html
    assert "1.4 + Loader 2.1" in html


def test_alumno_sin_inscripcion_no_ve_la_guia(client, guide, steps):
    client.force_login(make_user("sin-acceso@example.com"))

    assert client.get(guide_url(guide)).status_code == 403


def test_inscripcion_vencida_no_ve_la_guia(client, guide, steps, course):
    user = make_user("vencido@example.com")
    enrol(user, course, access_ends_at=timezone.now() - timedelta(days=1))
    client.force_login(user)

    assert client.get(guide_url(guide)).status_code == 403


def test_marca_y_desmarca_un_paso(client, guide, steps, course):
    user = make_user("alumno@example.com")
    enrol(user, course)
    client.force_login(user)
    first, _second = steps

    response = client.post(toggle_url(first))

    assert response.status_code == 302
    assert LabStepProgress.objects.filter(user=user, step=first).exists()

    client.post(toggle_url(first))

    assert not LabStepProgress.objects.filter(user=user, step=first).exists()


def test_un_alumno_sin_inscripcion_no_puede_marcar_pasos(client, guide, steps):
    user = make_user("sin-acceso@example.com")
    client.force_login(user)

    response = client.post(toggle_url(steps[0]))

    assert response.status_code == 403
    assert not LabStepProgress.objects.exists()


def test_no_se_marca_un_paso_de_otra_guia(client, guide, steps, course):
    other_game = Game.objects.create(
        name="Otro", slug="otro", description="Otro.", official_url="https://example.com/"
    )
    other_version = GameVersion.objects.create(
        game=other_game, number="1.0", release_date=date(2026, 1, 1)
    )
    other_environment = ModdingEnvironment.objects.create(
        game=other_game, name="Otro loader", version="1.0"
    )
    other_guide = LabGuide.objects.create(
        game=other_game,
        game_version=other_version,
        modding_environment=other_environment,
        requirements="x",
        final_check="y",
    )
    other_step = LabStep.objects.create(guide=other_guide, order=1, title="Ajeno", instructions="x")
    user = make_user("alumno@example.com")
    enrol(user, course)
    client.force_login(user)

    response = client.post(
        reverse("enrollments:toggle_lab_step", args=[guide.game.slug, other_step.pk])
    )

    assert response.status_code == 404
    assert not LabStepProgress.objects.exists()


def test_el_tutor_ve_quien_esta_atorado(client, guide, steps, course):
    first, second = steps
    advanced = make_user("avanzada@example.com")
    stuck = make_user("atorado@example.com")
    enrol(advanced, course)
    enrol(stuck, course)
    LabStepProgress.objects.create(user=advanced, step=first)
    tutor = make_user("tutor@example.com", is_tutor=True)
    client.force_login(tutor)

    html = client.get(guide_url(guide)).content.decode()

    assert "Quién está atorado" in html
    assert "avanzada@example.com" in html
    assert "atorado@example.com" in html
    assert "1 / 2" in html
    assert second.title in html
    # El tutor no marca pasos: la guía es de los alumnos.
    assert "Marcar como hecho" not in html


def test_el_tutor_no_puede_marcar_pasos(client, guide, steps, course):
    tutor = make_user("tutor@example.com", is_tutor=True)
    client.force_login(tutor)

    response = client.post(toggle_url(steps[0]))

    assert response.status_code == 403
    assert not LabStepProgress.objects.exists()


def test_el_tutor_ve_la_lista_de_guias(client, guide, steps):
    client.force_login(make_user("tutor@example.com", is_tutor=True))

    html = client.get(reverse("labs:guides")).content.decode()

    assert "Juego de prueba" in html
    assert "2 pasos" in html


def test_un_alumno_no_entra_a_la_lista_de_guias(client, guide, steps):
    client.force_login(make_user("alumno@example.com"))

    assert client.get(reverse("labs:guides")).status_code == 403
