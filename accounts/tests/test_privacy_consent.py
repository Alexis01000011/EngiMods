from datetime import timedelta

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.urls import reverse
from django.utils import timezone

from accounts.models import PrivacyConsent, User
from core.models import LegalText

pytestmark = pytest.mark.django_db


@pytest.fixture
def aviso():
    return LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="1.0",
        body="Texto del aviso.",
        effective_date=timezone.localdate(),
    )


@pytest.fixture
def alumno():
    return User.objects.create_user(email="alumno@x.com", password="x", display_name="Alumno")


def test_registra_quien_acepto_que_version_y_cuando(aviso, alumno):
    antes = timezone.now()
    consent = PrivacyConsent.objects.create(user=alumno, legal_text=aviso)
    assert consent.user == alumno
    assert consent.legal_text == aviso
    assert antes <= consent.accepted_at <= timezone.now()
    assert list(alumno.privacy_consents.all()) == [consent]


def test_sin_cuenta_se_registra_ligado_al_correo(aviso):
    consent = PrivacyConsent.objects.create(email="interesada@x.com", legal_text=aviso)
    assert consent.user is None
    assert consent.email == "interesada@x.com"
    assert str(consent) == "interesada@x.com · Aviso de privacidad 1.0"


def test_el_consentimiento_necesita_usuario_o_correo(aviso):
    with pytest.raises(IntegrityError):
        PrivacyConsent.objects.create(legal_text=aviso)


def test_el_consentimiento_no_lleva_usuario_y_correo_a_la_vez(aviso, alumno):
    with pytest.raises(IntegrityError):
        PrivacyConsent.objects.create(user=alumno, email="otro@x.com", legal_text=aviso)


def test_cada_version_aceptada_queda_registrada(aviso, alumno):
    nueva = LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="2.0",
        body="Texto nuevo.",
        effective_date=timezone.localdate() + timedelta(days=1),
    )
    PrivacyConsent.objects.create(user=alumno, legal_text=aviso)
    PrivacyConsent.objects.create(user=alumno, legal_text=nueva)
    versiones = set(alumno.privacy_consents.values_list("legal_text__version", flat=True))
    assert versiones == {"1.0", "2.0"}


def test_no_se_borra_una_version_que_alguien_acepto(aviso, alumno):
    PrivacyConsent.objects.create(user=alumno, legal_text=aviso)
    with pytest.raises(ProtectedError):
        aviso.delete()


def test_al_borrar_la_cuenta_se_borran_sus_consentimientos(aviso, alumno):
    PrivacyConsent.objects.create(user=alumno, legal_text=aviso)
    alumno.delete()
    assert not PrivacyConsent.objects.exists()


def test_el_admin_lista_consentimientos_en_solo_lectura(client, aviso, alumno):
    PrivacyConsent.objects.create(user=alumno, legal_text=aviso)
    admin_user = User.objects.create_superuser(email="admin@x.com", password="x", display_name="A")
    client.force_login(admin_user)

    response = client.get(reverse("admin:accounts_privacyconsent_changelist"))
    assert response.status_code == 200
    assert "alumno@x.com" in response.content.decode()

    response = client.get(reverse("admin:accounts_privacyconsent_add"))
    assert response.status_code == 403


def test_un_alumno_no_ve_los_consentimientos_en_el_admin(client, alumno):
    client.force_login(alumno)
    response = client.get(reverse("admin:accounts_privacyconsent_changelist"))
    assert response.status_code == 302
