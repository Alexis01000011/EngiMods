import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import path, reverse
from django.views import View

from accounts.permissions import TutorRequiredMixin, has_tutor_access, tutor_required

pytestmark = pytest.mark.django_db


@tutor_required
def tutor_view(request):
    return HttpResponse("OK")


class TutorView(TutorRequiredMixin, View):
    def get(self, request):
        return HttpResponse("OK")


urlpatterns = [
    path("tutoria/funcion/", tutor_view),
    path("tutoria/clase/", TutorView.as_view()),
]


@pytest.mark.parametrize("route", ["/tutoria/funcion/", "/tutoria/clase/"])
@pytest.mark.parametrize(
    ("role", "flags", "status"),
    [
        ("anonimo", None, 403),
        ("alumno", {}, 403),
        ("personal", {"is_staff": True}, 403),
        ("tutor", {"is_tutor": True}, 200),
        ("superusuario", {"is_superuser": True}, 200),
        ("tutor_inactivo", {"is_tutor": True, "is_active": False}, 403),
        ("superusuario_inactivo", {"is_superuser": True, "is_active": False}, 403),
    ],
)
def test_pantallas_de_tutor_comparten_permisos(client, settings, route, role, flags, status):
    settings.ROOT_URLCONF = __name__
    if flags is not None:
        user = get_user_model().objects.create_user(
            email=f"{role}@example.com", display_name=role, **flags
        )
        client.force_login(user)
    response = client.get(route)
    assert response.status_code == status
    if status == 200:
        assert response.content == b"OK"


def test_el_usuario_nuevo_no_es_tutor():
    user = get_user_model().objects.create_user(email="alumno@example.com", display_name="Alumno")
    assert not user.is_tutor
    assert not has_tutor_access(user)


def test_la_proteccion_rechaza_usuarios_inactivos_sin_depender_del_backend():
    user = get_user_model()(is_tutor=True, is_active=False)
    request = RequestFactory().get("/tutoria/")
    request.user = user
    with pytest.raises(PermissionDenied):
        tutor_view(request)
    with pytest.raises(PermissionDenied):
        TutorView.as_view()(request)
    assert not has_tutor_access(AnonymousUser())


@pytest.mark.parametrize("is_tutor", [True, False])
def test_admin_puede_marcar_y_desmarcar_tutor(admin_client, is_tutor):
    user = get_user_model().objects.create_user(
        email="tutor@example.com", display_name="Tutor", is_tutor=not is_tutor
    )
    data = {
        "email": user.email,
        "display_name": user.display_name,
        "is_active": "on",
        "date_joined_0": user.date_joined.strftime("%Y-%m-%d"),
        "date_joined_1": user.date_joined.strftime("%H:%M:%S"),
    }
    if is_tutor:
        data["is_tutor"] = "on"
    response = admin_client.post(reverse("admin:accounts_user_change", args=[user.pk]), data)
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.is_tutor is is_tutor
    assert not user.is_staff


def test_admin_filtra_tutores(admin_client):
    tutor = get_user_model().objects.create_user(
        email="tutor@example.com", display_name="Tutor", is_tutor=True
    )
    response = admin_client.get(reverse("admin:accounts_user_changelist"), {"is_tutor__exact": "1"})
    assert list(response.context["cl"].queryset) == [tutor]


def test_el_tutor_no_puede_asignar_su_rol_desde_el_admin(client):
    user = get_user_model().objects.create_user(
        email="tutor@example.com", display_name="Tutor", is_tutor=True
    )
    client.force_login(user)
    response = client.post(
        reverse("admin:accounts_user_change", args=[user.pk]), {"is_staff": "on"}
    )
    assert response.status_code == 302
    user.refresh_from_db()
    assert not user.is_staff
