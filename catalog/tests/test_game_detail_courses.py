"""Página pública de cada juego con sus cursos publicados (EM-012)."""

from datetime import date

import pytest
from django.urls import reverse

from catalog.models import Game, GameVersion
from courses.models import Course

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego para probar la página pública.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def otro_juego():
    return Game.objects.create(
        name="Otro juego",
        slug="otro-juego",
        description="Otro juego de prueba.",
        official_url="https://example.org/",
        status=Game.Status.ACTIVE,
    )


def crear_curso(game, titulo="Curso de prueba", slug="curso-de-prueba", estado=None):
    return Course.objects.create(
        title=titulo,
        slug=slug,
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Un curso para probar la página del juego.",
        requirements="Computadora y el juego.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=estado or Course.Status.PUBLISHED,
    )


def test_la_url_del_detalle_esta_en_espanol(game):
    assert game.get_absolute_url() == "/juegos/juego-de-prueba/"


def test_el_detalle_muestra_solo_los_cursos_publicados_del_juego(client, game, otro_juego):
    publicado = crear_curso(game)
    crear_curso(
        game, titulo="Curso en borrador", slug="curso-en-borrador", estado=Course.Status.DRAFT
    )
    crear_curso(otro_juego, titulo="Curso de otro juego", slug="curso-de-otro-juego")

    content = client.get(game.get_absolute_url()).content.decode()

    assert publicado.title in content
    assert reverse("courses:course_detail", kwargs={"slug": publicado.slug}) in content
    assert "Curso en borrador" not in content
    assert "Curso de otro juego" not in content


def test_el_detalle_con_cursos_no_muestra_el_estado_vacio(client, game):
    crear_curso(game)
    content = client.get(game.get_absolute_url()).content.decode()
    assert "todavía no tiene cursos publicados." not in content


def test_sin_cursos_lo_indica_y_ofrece_la_lista_de_espera_del_juego(client, game):
    content = client.get(game.get_absolute_url()).content.decode()
    assert "todavía no tiene cursos publicados." in content
    assert "Dejar mi correo en la lista de espera" in content
    esperado = f"{reverse('waitlist:join')}?juego={game.slug}"
    assert esperado in content


def test_con_cursos_el_enlace_de_la_lista_de_espera_conserva_el_juego(client, game):
    crear_curso(game)
    content = client.get(game.get_absolute_url()).content.decode()
    assert f"{reverse('waitlist:join')}?juego={game.slug}" in content


def test_el_detalle_muestra_la_version_actual_soportada(client, game):
    GameVersion.objects.create(game=game, number="1.3.0", release_date=date(2026, 6, 15))
    GameVersion.objects.create(
        game=game, number="1.4.2", release_date=date(2026, 10, 1), is_current=True
    )
    content = client.get(game.get_absolute_url()).content.decode()
    assert "1.4.2" in content
    assert "Versión actual" in content


def test_un_juego_oculto_no_muestra_sus_cursos(client, game):
    crear_curso(game)
    game.status = Game.Status.HIDDEN
    game.save()
    assert client.get(game.get_absolute_url()).status_code == 404


def test_el_listado_sigue_mostrando_solo_juegos_activos(client, game, otro_juego):
    otro_juego.status = Game.Status.HIDDEN
    otro_juego.save()
    content = client.get(reverse("catalog:game_list")).content.decode()
    assert game.name in content
    assert otro_juego.name not in content
