"""Inicio de sesión, cierre y recuperación de contraseña (EM-031)."""

import re
from datetime import timedelta

import pytest
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import PrivacyConsent, User
from accounts.tokens import email_verification_token
from core.models import LegalText

pytestmark = pytest.mark.django_db

LOGIN_URL = reverse("accounts:login")
LOGOUT_URL = reverse("accounts:logout")
ACCEPT_URL = reverse("accounts:accept_privacy")
RESET_URL = reverse("accounts:password_reset")
MY_COURSES_URL = reverse("enrollments:my_courses")
PASSWORD = "una-clave-larga-42"


def aviso(version, days_ago=0):
    return LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version=version,
        body="Texto del aviso.",
        effective_date=timezone.localdate() - timedelta(days=days_ago),
    )


@pytest.fixture
def alumna():
    return User.objects.create_user(
        email="alumna@example.com", password=PASSWORD, display_name="Alumna"
    )


def link_del_correo(message):
    return re.search(r"https?://\S+", message.body).group(0)


# Inicio de sesión con correo y contraseña


def test_el_formulario_pide_correo_y_contraseña(client):
    response = client.get(LOGIN_URL)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'type="email"' in html
    assert "Correo" in html
    assert "Contraseña" in html
    assert reverse("accounts:password_reset") in html


def test_entra_con_correo_y_contraseña_y_va_a_mi_panel(client, alumna):
    response = client.post(LOGIN_URL, {"username": "alumna@example.com", "password": PASSWORD})
    assert response.status_code == 302
    assert response.url == MY_COURSES_URL
    assert client.session["_auth_user_id"] == str(alumna.pk)


def test_el_correo_no_distingue_mayusculas(client, alumna):
    client.post(LOGIN_URL, {"username": "Alumna@Example.com", "password": PASSWORD})
    assert client.session["_auth_user_id"] == str(alumna.pk)


def test_vuelve_a_la_pagina_que_pedia_sesion(client, alumna):
    response = client.get(MY_COURSES_URL)
    assert response.status_code == 302
    assert response.url.startswith(LOGIN_URL)

    response = client.post(
        f"{LOGIN_URL}?next={MY_COURSES_URL}",
        {"username": "alumna@example.com", "password": PASSWORD, "next": MY_COURSES_URL},
    )
    assert response.url == MY_COURSES_URL


def test_no_redirige_a_otro_sitio(client, alumna):
    response = client.post(
        LOGIN_URL,
        {"username": "alumna@example.com", "password": PASSWORD, "next": "https://otro.example"},
    )
    assert response.url == MY_COURSES_URL


def test_contraseña_equivocada_muestra_error_en_español_sin_revelar_la_cuenta(client, alumna):
    equivocada = client.post(LOGIN_URL, {"username": "alumna@example.com", "password": "otra"})
    sin_cuenta = client.post(LOGIN_URL, {"username": "nadie@example.com", "password": "otra"})
    assert equivocada.status_code == sin_cuenta.status_code == 200
    assert "_auth_user_id" not in client.session
    mensaje = "El correo o la contraseña no coinciden."
    assert mensaje in equivocada.content.decode()
    assert mensaje in sin_cuenta.content.decode()


def test_una_cuenta_desactivada_no_entra(client, alumna):
    alumna.is_active = False
    alumna.save()
    client.post(LOGIN_URL, {"username": "alumna@example.com", "password": PASSWORD})
    assert "_auth_user_id" not in client.session


def test_con_sesion_iniciada_la_pantalla_de_entrar_manda_a_mi_panel(client, alumna):
    client.force_login(alumna)
    response = client.get(LOGIN_URL)
    assert response.status_code == 302
    assert response.url == MY_COURSES_URL


# Cierre de sesión


def test_salir_cierra_la_sesion(client, alumna):
    client.force_login(alumna)
    response = client.post(LOGOUT_URL, follow=True)
    assert "_auth_user_id" not in client.session
    assert response.redirect_chain[-1][0] == reverse("core:home")
    assert "Cerraste tu sesión." in response.content.decode()


def test_salir_no_se_puede_por_get(client, alumna):
    client.force_login(alumna)
    response = client.get(LOGOUT_URL)
    assert response.status_code == 405
    assert client.session["_auth_user_id"] == str(alumna.pk)


def test_la_barra_muestra_entrar_o_salir(client, alumna):
    html = client.get(reverse("core:home")).content.decode()
    assert LOGIN_URL in html
    assert LOGOUT_URL not in html

    client.force_login(alumna)
    html = client.get(reverse("core:home")).content.decode()
    assert LOGOUT_URL in html
    assert f'href="{LOGIN_URL}"' not in html


# Aviso de privacidad nuevo al iniciar sesión


def login(client):
    return client.post(LOGIN_URL, {"username": "alumna@example.com", "password": PASSWORD})


def test_si_ya_acepto_la_version_vigente_no_se_le_pide(client, alumna):
    vigente = aviso("1.0")
    PrivacyConsent.objects.create(user=alumna, legal_text=vigente)
    assert login(client).url == MY_COURSES_URL


def test_sin_aviso_publicado_entra_directo(client, alumna):
    assert login(client).url == MY_COURSES_URL


def test_si_cambio_la_version_se_pide_aceptarla_al_entrar(client, alumna):
    anterior = aviso("1.0", days_ago=30)
    PrivacyConsent.objects.create(user=alumna, legal_text=anterior)
    aviso("2.0")

    response = login(client)
    assert response.status_code == 302
    assert response.url.startswith(ACCEPT_URL)

    response = client.get(response.url)
    assert response.status_code == 200
    html = response.content.decode()
    assert "Actualizamos el aviso de privacidad" in html
    assert "versión 2.0" in html


def test_aceptar_guarda_la_version_vigente_y_sigue_al_destino(client, alumna):
    aviso("1.0", days_ago=30)
    vigente = aviso("2.0")
    client.force_login(alumna)

    response = client.post(ACCEPT_URL, {"accept_privacy": "on", "next": MY_COURSES_URL})
    assert response.status_code == 302
    assert response.url == MY_COURSES_URL
    assert PrivacyConsent.objects.filter(user=alumna, legal_text=vigente).exists()


def test_sin_marcar_la_casilla_no_se_acepta(client, alumna):
    aviso("1.0")
    client.force_login(alumna)
    response = client.post(ACCEPT_URL, {})
    assert response.status_code == 200
    assert "Para seguir, acepta el aviso de privacidad." in response.content.decode()
    assert not PrivacyConsent.objects.exists()


def test_aceptar_no_redirige_a_otro_sitio(client, alumna):
    aviso("1.0")
    client.force_login(alumna)
    response = client.post(ACCEPT_URL, {"accept_privacy": "on", "next": "https://otro.example"})
    assert response.url == MY_COURSES_URL


def test_si_ya_acepto_la_pantalla_de_aceptar_lo_deja_pasar(client, alumna):
    vigente = aviso("1.0")
    PrivacyConsent.objects.create(user=alumna, legal_text=vigente)
    client.force_login(alumna)
    response = client.get(ACCEPT_URL)
    assert response.status_code == 302
    assert PrivacyConsent.objects.count() == 1


def test_aceptar_el_aviso_pide_sesion(client):
    aviso("1.0")
    response = client.get(ACCEPT_URL)
    assert response.status_code == 302
    assert response.url.startswith(LOGIN_URL)


# Recuperación de contraseña por correo con enlace que expira


def test_pide_el_enlace_y_llega_un_correo_en_español(client, alumna):
    response = client.post(RESET_URL, {"email": "alumna@example.com"})
    assert response.status_code == 302
    assert response.url == reverse("accounts:password_reset_done")
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.to == ["alumna@example.com"]
    assert message.subject == "Recupera tu contraseña de EngiMods"
    assert "Hola, Alumna:" in message.body
    assert "El enlace vence en" in message.body
    assert "/recuperar-contrasena/" in link_del_correo(message)


def test_un_correo_sin_cuenta_ve_lo_mismo_y_no_recibe_nada(client, alumna):
    response = client.post(RESET_URL, {"email": "nadie@example.com"})
    assert response.url == reverse("accounts:password_reset_done")
    assert mail.outbox == []


def test_el_enlace_permite_elegir_una_contraseña_nueva(client, alumna):
    client.post(RESET_URL, {"email": "alumna@example.com"})
    response = client.get(link_del_correo(mail.outbox[0]), follow=True)
    assert "Elige tu contraseña nueva" in response.content.decode()

    set_password_url = response.redirect_chain[-1][0]
    nueva = "otra-clave-larga-73"
    response = client.post(set_password_url, {"new_password1": nueva, "new_password2": nueva})
    assert response.url == reverse("accounts:password_reset_complete")
    alumna.refresh_from_db()
    assert alumna.check_password(nueva)


def test_el_enlace_sirve_una_sola_vez(client, alumna):
    client.post(RESET_URL, {"email": "alumna@example.com"})
    link = link_del_correo(mail.outbox[0])
    response = client.get(link, follow=True)
    nueva = "otra-clave-larga-73"
    client.post(response.redirect_chain[-1][0], {"new_password1": nueva, "new_password2": nueva})

    response = client.get(link, follow=True)
    assert "El enlace ya no sirve" in response.content.decode()


def test_el_enlace_vence(client, alumna):
    client.post(RESET_URL, {"email": "alumna@example.com"})
    link = link_del_correo(mail.outbox[0])
    with override_settings(PASSWORD_RESET_TIMEOUT=-1):
        response = client.get(link, follow=True)
    assert "El enlace ya no sirve" in response.content.decode()
    alumna.refresh_from_db()
    assert alumna.check_password(PASSWORD)


def test_el_enlace_de_verificar_correo_no_cambia_la_contraseña(client, alumna):
    uid = urlsafe_base64_encode(force_bytes(alumna.pk))
    url = reverse(
        "accounts:password_reset_confirm", args=[uid, email_verification_token.make_token(alumna)]
    )
    response = client.get(url, follow=True)
    assert "El enlace ya no sirve" in response.content.decode()


def test_la_contraseña_nueva_muestra_errores_en_español(client, alumna):
    client.post(RESET_URL, {"email": "alumna@example.com"})
    response = client.get(link_del_correo(mail.outbox[0]), follow=True)
    response = client.post(
        response.redirect_chain[-1][0], {"new_password1": "abc", "new_password2": "xyz"}
    )
    assert response.status_code == 200
    assert "No se pudo cambiar tu contraseña." in response.content.decode()
