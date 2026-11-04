import pytest
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError
from django.db.migrations.loader import MigrationLoader
from django.urls import reverse

from accounts.models import User

pytestmark = pytest.mark.django_db


def test_auth_user_model_es_el_de_accounts():
    assert settings.AUTH_USER_MODEL == "accounts.User"
    assert get_user_model() is User


def test_el_modelo_no_tiene_username_y_usa_el_correo():
    field_names = {f.name for f in User._meta.get_fields()}
    assert "username" not in field_names
    assert User.USERNAME_FIELD == "email"
    assert "display_name" in User.REQUIRED_FIELDS


def test_create_user_con_correo_y_nombre_a_mostrar():
    user = User.objects.create_user(
        email="ana@ejemplo.com", password="x-Segura-123", display_name="Ana"
    )
    assert user.email == "ana@ejemplo.com"
    assert user.display_name == "Ana"
    assert user.check_password("x-Segura-123")
    assert not user.is_staff
    assert str(user) == "ana@ejemplo.com"


def test_create_user_sin_correo_falla():
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="x", display_name="Ana")


def test_create_superuser():
    user = User.objects.create_superuser(email="admin@ejemplo.com", password="x", display_name="A")
    assert user.is_staff
    assert user.is_superuser


def test_createsuperuser_pide_correo():
    call_command(
        "createsuperuser",
        interactive=False,
        email="root@ejemplo.com",
        display_name="Root",
        verbosity=0,
    )
    assert User.objects.get(email="root@ejemplo.com").is_superuser


def test_correo_unico_sin_distinguir_mayusculas_en_base_de_datos():
    User.objects.create_user(email="ana@x.com", password="x", display_name="Ana")
    with pytest.raises(IntegrityError):
        User.objects.create_user(email="Ana@x.com", password="x", display_name="Otra Ana")


def test_correo_duplicado_con_mayusculas_da_error_de_validacion():
    User.objects.create_user(email="ana@x.com", password="x", display_name="Ana")
    otro = User(email="ANA@x.com", display_name="Otra Ana")
    with pytest.raises(ValidationError):
        otro.full_clean()


def test_inicio_de_sesion_con_correo_sin_distinguir_mayusculas():
    User.objects.create_user(email="ana@x.com", password="x-Segura-123", display_name="Ana")
    assert authenticate(username="Ana@X.com", password="x-Segura-123") is not None
    assert authenticate(username="ana@x.com", password="incorrecta") is None


def test_el_usuario_esta_registrado_en_el_admin():
    assert admin.site.is_registered(User)


def test_admin_crea_usuario_con_correo(client):
    admin_user = User.objects.create_superuser(email="admin@x.com", password="x", display_name="A")
    client.force_login(admin_user)
    response = client.post(
        reverse("admin:accounts_user_add"),
        {
            "email": "nuevo@x.com",
            "display_name": "Nuevo",
            "password1": "Una-clave-larga-123",
            "password2": "Una-clave-larga-123",
            "usable_password": "true",
        },
    )
    assert response.status_code == 302
    assert User.objects.filter(email="nuevo@x.com").exists()


def test_admin_lista_usuarios(client):
    admin_user = User.objects.create_superuser(email="admin@x.com", password="x", display_name="A")
    client.force_login(admin_user)
    response = client.get(reverse("admin:accounts_user_changelist"))
    assert response.status_code == 200
    assert "admin@x.com" in response.content.decode()


def test_un_alumno_no_entra_al_admin_de_usuarios(client):
    alumno = User.objects.create_user(email="alumno@x.com", password="x", display_name="Alumno")
    client.force_login(alumno)
    response = client.get(reverse("admin:accounts_user_changelist"))
    assert response.status_code == 302


def test_es_la_primera_migracion_del_proyecto():
    """accounts.0001 es inicial y no depende de migraciones de otras apps del proyecto."""
    loader = MigrationLoader(None, ignore_no_migrations=True)
    key = ("accounts", "0001_initial")
    assert loader.graph.nodes[key].initial
    previous = [node for node in loader.graph.forwards_plan(key) if node != key]
    assert all(app.startswith(("auth", "contenttypes")) for app, _name in previous)
