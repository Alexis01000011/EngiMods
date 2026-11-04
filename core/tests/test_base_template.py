"""Plantilla base (EM-004): estilos, navegación, mensajes y pie."""

import pytest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone

from config.urls import urlpatterns as project_urlpatterns
from core.models import LegalText

pytestmark = pytest.mark.django_db


def messages_view(request):
    messages.success(request, "Pago confirmado.")
    messages.error(request, "No se pudo guardar.")
    return render(request, "core/home.html")


urlpatterns = [path("prueba/mensajes/", messages_view), *project_urlpatterns]


def make_user(**kwargs):
    return get_user_model().objects.create_user(
        email="persona@example.com", password="x-12345678", **kwargs
    )


def page(client, name="core:home"):
    return client.get(reverse(name)).content.decode()


def test_carga_la_hoja_de_estilos_y_se_adapta_al_telefono(client):
    html = page(client)
    assert 'href="/static/css/tailwind.css"' in html
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html


def test_la_navegacion_lleva_al_inicio_y_a_los_juegos(client):
    html = page(client)
    assert f'href="{reverse("core:home")}"' in html
    assert f'href="{reverse("catalog:game_list")}"' in html
    assert 'href="#contenido"' in html
    assert 'id="contenido"' in html


def test_un_visitante_no_ve_mi_panel_ni_tutoria(client):
    html = page(client)
    assert reverse("enrollments:my_courses") not in html
    assert reverse("reviews:queue") not in html


def test_un_alumno_ve_mi_panel_pero_no_tutoria(client):
    client.force_login(make_user())
    html = page(client)
    assert f'href="{reverse("enrollments:my_courses")}"' in html
    assert reverse("reviews:queue") not in html


@pytest.mark.parametrize("flags", [{"is_tutor": True}, {"is_superuser": True}])
def test_un_tutor_ve_el_enlace_a_tutoria(client, flags):
    client.force_login(make_user(**flags))
    assert f'href="{reverse("reviews:queue")}"' in page(client)


def test_marca_la_seccion_actual_en_la_navegacion(client):
    assert 'aria-current="page"' not in page(client)
    # El enlace aparece dos veces: en línea en escritorio y en el menú del teléfono.
    assert page(client, "catalog:game_list").count('aria-current="page"') == 2


@pytest.mark.urls(__name__)
def test_muestra_los_mensajes_con_el_color_de_su_estado(client):
    html = client.get("/prueba/mensajes/").content.decode()
    assert "Pago confirmado." in html
    assert "No se pudo guardar." in html
    assert "bg-tested-container text-tested" in html
    assert "bg-error-container text-error" in html


def test_sin_mensajes_no_hay_seccion_de_mensajes(client):
    assert 'aria-label="Mensajes"' not in page(client)


def test_el_pie_enlaza_al_aviso_de_privacidad_solo_si_hay_version_vigente(client):
    enlace = f'href="{reverse("core:privacy")}"'
    assert enlace not in page(client)
    LegalText.objects.create(
        kind=LegalText.Kind.PRIVACY,
        version="1.0",
        body="Texto de prueba.",
        effective_date=timezone.localdate(),
    )
    assert enlace in page(client)
