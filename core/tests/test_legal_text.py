from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone

from core.models import LegalText

pytestmark = pytest.mark.django_db

PRIVACY = LegalText.Kind.PRIVACY


def _privacy(version, days_from_today=0, body="Texto del aviso."):
    return LegalText.objects.create(
        kind=PRIVACY,
        version=version,
        body=body,
        effective_date=timezone.localdate() + timedelta(days=days_from_today),
    )


def test_la_version_vigente_es_la_mas_reciente_que_ya_llego():
    _privacy("1.0", days_from_today=-30)
    actual = _privacy("1.1", days_from_today=-1)
    _privacy("2.0", days_from_today=10)
    assert LegalText.objects.current(PRIVACY) == actual


def test_una_version_entra_en_vigor_el_dia_de_su_fecha():
    hoy = _privacy("1.0", days_from_today=0)
    assert LegalText.objects.current(PRIVACY) == hoy


def test_sin_versiones_vigentes_no_hay_aviso():
    assert LegalText.objects.current(PRIVACY) is None
    _privacy("1.0", days_from_today=5)
    assert LegalText.objects.current(PRIVACY) is None


def test_no_se_repite_una_version_del_mismo_tipo():
    _privacy("1.0")
    with pytest.raises(IntegrityError):
        _privacy("1.0", days_from_today=-3)


def test_privacidad_muestra_la_version_vigente_a_un_visitante(client):
    _privacy("1.0", days_from_today=-30, body="Aviso anterior.")
    _privacy("1.1", days_from_today=-1, body="Guardamos tu correo para tu cuenta.")
    _privacy("2.0", days_from_today=10, body="Aviso que aún no rige.")

    response = client.get(reverse("core:privacy"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Aviso de privacidad" in content
    assert "Versión 1.1" in content
    assert "Guardamos tu correo para tu cuenta." in content
    assert "Aviso anterior." not in content
    assert "Aviso que aún no rige." not in content


def test_privacidad_muestra_la_fecha_de_vigencia_en_espanol(client):
    LegalText.objects.create(
        kind=PRIVACY, version="1.0", body="Texto.", effective_date=date(2026, 11, 2)
    )
    content = client.get(reverse("core:privacy")).content.decode()
    assert "vigente desde el 2 de noviembre de 2026" in content


def test_la_url_de_privacidad_esta_en_espanol():
    assert reverse("core:privacy") == "/privacidad/"


def test_privacidad_sin_aviso_vigente_da_404(client):
    _privacy("1.0", days_from_today=5)
    response = client.get(reverse("core:privacy"))
    assert response.status_code == 404


def test_privacidad_escapa_el_html_del_texto(client):
    _privacy("1.0", body="<script>alert('x')</script>")
    content = client.get(reverse("core:privacy")).content.decode()
    assert "<script>" not in content
    assert "&lt;script&gt;" in content


def test_el_administrador_captura_una_version_en_el_admin(client):
    admin_user = get_user_model().objects.create_superuser(
        email="admin@x.com", password="x", display_name="A"
    )
    client.force_login(admin_user)
    response = client.post(
        reverse("admin:core_legaltext_add"),
        {
            "kind": PRIVACY,
            "version": "1.0",
            "body": "Texto capturado en el admin.",
            "effective_date": timezone.localdate().isoformat(),
        },
    )
    assert response.status_code == 302
    assert LegalText.objects.current(PRIVACY).body == "Texto capturado en el admin."


def test_el_admin_lista_versiones_y_marca_la_vigente(client):
    _privacy("1.0", days_from_today=-30)
    _privacy("1.1", days_from_today=-1)
    admin_user = get_user_model().objects.create_superuser(
        email="admin@x.com", password="x", display_name="A"
    )
    client.force_login(admin_user)
    response = client.get(reverse("admin:core_legaltext_changelist"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "1.0" in content
    assert "1.1" in content
    assert content.count("icon-yes.svg") == 1
    assert content.count("icon-no.svg") == 1


def test_un_alumno_no_entra_al_admin_de_textos_legales(client):
    alumno = get_user_model().objects.create_user(
        email="alumno@x.com", password="x", display_name="Alumno"
    )
    client.force_login(alumno)
    response = client.get(reverse("admin:core_legaltext_changelist"))
    assert response.status_code == 302
