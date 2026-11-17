"""Pantallas del catálogo con la identidad visual (EM-015)."""

from datetime import date

import pytest
from django.urls import reverse

from catalog.models import Game, GameVersion, ModdingEnvironment

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego para probar el catálogo.",
        official_url="https://example.com/",
        logo_url="https://example.com/logo.png",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def versions(game):
    old = GameVersion.objects.create(game=game, number="1.3.0", release_date=date(2026, 6, 15))
    current = GameVersion.objects.create(
        game=game, number="1.4.2", release_date=date(2026, 10, 1), is_current=True
    )
    loader = ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9.1")
    loader.compatible_versions.set([old, current])
    sdk = ModdingEnvironment.objects.create(game=game, name="SDK", version="2.0")
    sdk.compatible_versions.set([current])
    return current, old


def rows(content):
    """Las filas del cuerpo de la tabla de versiones, en orden."""
    body = content.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    return body.split("<tr>")[1:]


def test_tarjeta_con_versiones_y_entornos_sin_logo(client, game, versions):
    content = client.get(reverse("catalog:game_list")).content.decode()
    assert "1.4.2 · actual" in content
    assert "1.3.0" in content
    assert "Loader 0.9.1" in content
    assert "SDK 2.0" in content
    assert game.logo_url not in content


def test_tarjeta_de_juego_sin_versiones(client, game):
    content = client.get(reverse("catalog:game_list")).content.decode()
    assert "Sin versiones registradas" in content


def test_detalle_con_tabla_de_versiones_de_la_mas_nueva_a_la_mas_vieja(client, game, versions):
    content = client.get(game.get_absolute_url()).content.decode()
    assert 'role="region"' in content
    current_row, old_row = rows(content)
    assert "1.4.2" in current_row
    assert "1 de octubre de 2026" in current_row
    assert "Loader 0.9.1" in current_row
    assert "SDK 2.0" in current_row
    assert "Versión actual" in current_row
    assert "1.3.0" in old_row
    assert "Loader 0.9.1" in old_row
    assert "SDK 2.0" not in old_row
    assert "Anterior" in old_row


def test_detalle_sin_versiones(client, game):
    content = client.get(game.get_absolute_url()).content.decode()
    assert "Aún no registramos versiones de este juego." in content
    assert "<table" not in content


def test_detalle_no_muestra_versiones_de_otro_juego(client, game, versions):
    other = Game.objects.create(
        name="Otro juego",
        slug="otro-juego",
        description="Otro.",
        official_url="https://example.org/",
        status=Game.Status.ACTIVE,
    )
    GameVersion.objects.create(game=other, number="9.9.9", release_date=date(2026, 1, 1))
    content = client.get(game.get_absolute_url()).content.decode()
    assert "9.9.9" not in content
