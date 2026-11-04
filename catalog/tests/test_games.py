import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse

from catalog.models import Game

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego para probar el catálogo.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


def test_juego_con_logo_opcional_y_url_publica(game):
    game.full_clean()
    assert str(game) == "Juego de prueba"
    assert game.logo_url == ""
    assert game.get_absolute_url() == "/juegos/juego-de-prueba/"


def test_slug_unico_en_base_de_datos(game):
    with pytest.raises(IntegrityError):
        Game.objects.create(slug=game.slug)


@pytest.mark.parametrize("field", ["official_url", "logo_url"])
def test_los_enlaces_deben_ser_urls_validas(game, field):
    setattr(game, field, "javascript:alert(1)")
    with pytest.raises(ValidationError) as error:
        game.full_clean()
    assert field in error.value.message_dict


def test_listado_publico_solo_muestra_juegos_activos(client, game):
    Game.objects.create(name="Juego oculto", slug="oculto", status=Game.Status.HIDDEN)
    response = client.get(reverse("catalog:game_list"))
    assert response.status_code == 200
    assert list(response.context["games"]) == [game]
    assert game.get_absolute_url() in response.content.decode()
    assert "Juego oculto" not in response.content.decode()


def test_listado_vacio(client):
    response = client.get(reverse("catalog:game_list"))
    assert "Todavía no hay juegos disponibles." in response.content.decode()


def test_detalle_publico_con_logo_url_y_descripcion_escapada(client, game):
    game.logo_url = "https://example.com/logo.png"
    game.description = "<script>alert(1)</script>"
    game.save()
    response = client.get(game.get_absolute_url())
    content = response.content.decode()
    assert response.status_code == 200
    assert game.name in content
    assert game.logo_url in content
    assert game.official_url in content
    assert "<script>" not in content
    assert "&lt;script&gt;" in content


def test_ocultar_juego_retira_listado_y_detalle(client, game):
    game.status = Game.Status.HIDDEN
    game.save()
    assert client.get(game.get_absolute_url()).status_code == 404
    assert game.name not in client.get(reverse("catalog:game_list")).content.decode()


def test_juego_inexistente_devuelve_404(client):
    assert (
        client.get(reverse("catalog:game_detail", kwargs={"slug": "no-existe"})).status_code == 404
    )


def test_administrador_crea_juego_desde_admin(admin_client):
    response = admin_client.post(
        reverse("admin:catalog_game_add"),
        {
            "name": "Otro juego",
            "slug": "otro-juego",
            "description": "Descripción breve.",
            "official_url": "https://example.com/",
            "logo_url": "https://example.com/logo.png",
            "status": Game.Status.ACTIVE,
        },
    )
    assert response.status_code == 302
    game = Game.objects.get(slug="otro-juego")
    assert game.logo_url == "https://example.com/logo.png"
    assert game.status == Game.Status.ACTIVE


def test_admin_filtra_por_estado_y_busca_por_nombre(admin_client, game):
    response = admin_client.get(
        reverse("admin:catalog_game_changelist"), {"status__exact": "hidden"}
    )
    assert response.status_code == 200
    assert game not in response.context["cl"].queryset
    response = admin_client.get(reverse("admin:catalog_game_changelist"), {"q": game.name})
    assert list(response.context["cl"].queryset) == [game]


@pytest.mark.parametrize("authenticated", [False, True])
def test_sin_permiso_no_se_puede_crear_juego(client, authenticated):
    if authenticated:
        user = get_user_model().objects.create_user(
            email="alumno@example.com", display_name="Alumno"
        )
        client.force_login(user)
    response = client.post(reverse("admin:catalog_game_add"), {"name": "No autorizado"})
    assert response.status_code == 302
    assert not Game.objects.exists()
