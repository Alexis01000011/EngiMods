"""Registro con correo y verificación (EM-030)."""

import re
from datetime import datetime, timedelta

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import PrivacyConsent, User
from accounts.tokens import EmailVerificationTokenGenerator, email_verification_token
from core.models import LegalText

pytestmark = pytest.mark.django_db

REGISTER_URL = reverse("accounts:register")


@pytest.fixture
def aviso():
    return LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="1.0",
        body="Texto del aviso.",
        effective_date=timezone.localdate(),
    )


def datos(**cambios):
    return {
        "email": "nueva@example.com",
        "display_name": "Nueva Alumna",
        "password1": "una-clave-larga-42",
        "password2": "una-clave-larga-42",
        "accept_privacy": "on",
        **cambios,
    }


def verify_url(user, token=None):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return reverse(
        "accounts:verify_email", args=[uid, token or email_verification_token.make_token(user)]
    )


def link_del_correo(message):
    return re.search(r"https?://\S+", message.body).group(0)


# Formulario de registro con correo, nombre a mostrar y contraseña


def test_el_formulario_pide_correo_nombre_contraseña_y_aviso(client, aviso):
    response = client.get(REGISTER_URL)
    assert response.status_code == 200
    html = response.content.decode()
    for name in ("email", "display_name", "password1", "password2", "accept_privacy"):
        assert f'name="{name}"' in html
    assert 'type="email"' in html
    assert 'type="password"' in html


def test_el_registro_crea_la_cuenta_e_inicia_sesion(client, aviso):
    response = client.post(REGISTER_URL, datos())
    assert response.status_code == 302
    assert response.url == reverse("enrollments:my_courses")
    user = User.objects.get(email="nueva@example.com")
    assert user.display_name == "Nueva Alumna"
    assert user.check_password("una-clave-larga-42")
    assert not user.is_tutor and not user.is_staff and not user.is_superuser
    assert client.session["_auth_user_id"] == str(user.pk)


def test_una_contraseña_debil_no_crea_la_cuenta(client, aviso):
    response = client.post(REGISTER_URL, datos(password1="12345678", password2="12345678"))
    assert response.status_code == 200
    assert not User.objects.exists()
    assert len(mail.outbox) == 0


def test_las_contraseñas_deben_coincidir(client, aviso):
    response = client.post(REGISTER_URL, datos(password2="otra-clave-larga-42"))
    assert response.status_code == 200
    assert not User.objects.exists()


def test_un_correo_incompleto_dice_como_escribirlo(client, aviso):
    response = client.post(REGISTER_URL, datos(email="nueva@"))
    assert "nombre@dominio.mx" in response.content.decode()
    assert not User.objects.exists()


def test_con_sesion_no_se_ve_el_registro(client, aviso):
    client.force_login(User.objects.create_user(email="ya@example.com", display_name="Ya"))
    response = client.get(REGISTER_URL)
    assert response.status_code == 302
    assert response.url == reverse("enrollments:my_courses")
    response = client.post(REGISTER_URL, datos())
    assert response.status_code == 302
    assert not User.objects.filter(email="nueva@example.com").exists()


def test_un_visitante_ve_el_enlace_para_crear_cuenta(client):
    html = client.get(reverse("core:home")).content.decode()
    assert f'href="{REGISTER_URL}"' in html


def test_con_sesion_no_aparece_el_enlace_para_crear_cuenta(client):
    client.force_login(User.objects.create_user(email="ya@example.com", display_name="Ya"))
    html = client.get(reverse("core:home")).content.decode()
    assert REGISTER_URL not in html


# Correo de verificación; sin verificar no se puede pagar


def test_el_registro_envia_el_enlace_de_verificacion(client, aviso):
    client.post(REGISTER_URL, datos())
    user = User.objects.get(email="nueva@example.com")
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.to == ["nueva@example.com"]
    assert message.subject == "Verifica tu correo en EngiMods"
    assert "Hola, Nueva Alumna:" in message.body
    assert link_del_correo(message) == f"http://testserver{verify_url(user)}"


def test_la_cuenta_nueva_no_esta_verificada_ni_puede_pagar(client, aviso):
    client.post(REGISTER_URL, datos())
    user = User.objects.get(email="nueva@example.com")
    assert user.email_verified_at is None
    assert user.can_pay is False


def test_el_enlace_del_correo_verifica_la_cuenta(client, aviso):
    client.post(REGISTER_URL, datos())
    client.logout()
    response = client.get(link_del_correo(mail.outbox[0]))
    assert response.status_code == 200
    assert "Tu correo está verificado" in response.content.decode()
    user = User.objects.get(email="nueva@example.com")
    assert user.email_verified_at is not None
    assert user.can_pay is True


def test_abrir_el_enlace_otra_vez_no_cambia_la_fecha(client):
    user = User.objects.create_user(email="ana@example.com", display_name="Ana")
    url = verify_url(user)
    client.get(url)
    user.refresh_from_db()
    primera = user.email_verified_at
    response = client.get(url)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.email_verified_at == primera


def test_un_enlace_alterado_no_verifica(client):
    user = User.objects.create_user(email="ana@example.com", display_name="Ana")
    response = client.get(verify_url(user, token="abc-123"))
    assert response.status_code == 400
    assert "No pudimos verificar tu correo" in response.content.decode()
    user.refresh_from_db()
    assert user.email_verified_at is None


def test_un_enlace_de_otra_cuenta_no_verifica(client):
    ana = User.objects.create_user(email="ana@example.com", display_name="Ana")
    beto = User.objects.create_user(email="beto@example.com", display_name="Beto")
    uid = urlsafe_base64_encode(force_bytes(beto.pk))
    token = email_verification_token.make_token(ana)
    response = client.get(reverse("accounts:verify_email", args=[uid, token]))
    assert response.status_code == 400
    beto.refresh_from_db()
    assert beto.email_verified_at is None


@pytest.mark.parametrize("uid", ["no-es-base64", urlsafe_base64_encode(b"999999")])
def test_un_enlace_de_una_cuenta_que_no_existe_no_verifica(client, uid):
    response = client.get(reverse("accounts:verify_email", args=[uid, "abc-123"]))
    assert response.status_code == 400


def test_un_enlace_vencido_no_verifica(client, settings, monkeypatch):
    user = User.objects.create_user(email="ana@example.com", display_name="Ana")
    url = verify_url(user)
    # El generador de Django mide el tiempo con fechas sin zona.
    later = datetime.now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT + 60)
    monkeypatch.setattr(EmailVerificationTokenGenerator, "_now", lambda self: later)
    response = client.get(url)
    assert response.status_code == 400
    user.refresh_from_db()
    assert user.email_verified_at is None


def test_el_enlace_deja_de_servir_si_cambia_el_correo(client):
    user = User.objects.create_user(email="ana@example.com", display_name="Ana")
    url = verify_url(user)
    user.email = "otra@example.com"
    user.save()
    response = client.get(url)
    assert response.status_code == 400
    user.refresh_from_db()
    assert user.email_verified_at is None


def test_un_token_de_recuperar_contraseña_no_verifica_el_correo(client):
    user = User.objects.create_user(email="ana@example.com", display_name="Ana")
    response = client.get(verify_url(user, token=default_token_generator.make_token(user)))
    assert response.status_code == 400


def test_una_cuenta_inactiva_no_puede_pagar_aunque_este_verificada():
    user = User.objects.create_user(
        email="ana@example.com",
        display_name="Ana",
        email_verified_at=timezone.now(),
        is_active=False,
    )
    assert user.can_pay is False


# Correo duplicado: error claro sin revelar datos de otra cuenta


def test_un_correo_duplicado_da_un_error_claro_sin_datos_de_la_otra_cuenta(client, aviso):
    User.objects.create_user(email="ana@example.com", display_name="Ana Secreta", password="x")
    response = client.post(REGISTER_URL, datos(email="ANA@example.com"))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Ya hay una cuenta con este correo." in html
    assert "Ana Secreta" not in html
    assert User.objects.count() == 1
    assert len(mail.outbox) == 0
    assert "_auth_user_id" not in client.session


# Aceptación del aviso de privacidad (EM-033)


def test_sin_aceptar_el_aviso_no_se_crea_la_cuenta(client, aviso):
    payload = datos()
    del payload["accept_privacy"]
    response = client.post(REGISTER_URL, payload)
    assert response.status_code == 200
    assert "acepta el aviso de privacidad" in response.content.decode()
    assert not User.objects.exists()


def test_el_formulario_enlaza_la_version_vigente_del_aviso(client, aviso):
    html = client.get(REGISTER_URL).content.decode()
    assert f'href="{reverse("core:privacy")}"' in html
    assert "versión 1.0" in html


def test_el_registro_guarda_la_version_vigente_que_se_acepto(client, aviso):
    LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="2.0",
        body="Versión futura.",
        effective_date=timezone.localdate() + timedelta(days=5),
    )
    client.post(REGISTER_URL, datos())
    consent = PrivacyConsent.objects.get()
    assert consent.user.email == "nueva@example.com"
    assert consent.legal_text == aviso


def test_sin_aviso_vigente_no_se_puede_registrar(client):
    response = client.get(REGISTER_URL)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Todavía no abrimos el registro." in html
    assert 'name="password1"' not in html
    client.post(REGISTER_URL, datos())
    assert not User.objects.exists()
    assert len(mail.outbox) == 0
