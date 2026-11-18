"""Listado público de cursos con filtros (EM-013)."""

import pytest
from django.urls import reverse

from catalog.models import Game
from courses.models import Course

pytestmark = pytest.mark.django_db


def make_game(name, slug, status=Game.Status.ACTIVE):
    return Game.objects.create(
        name=name,
        slug=slug,
        description=f"{name}.",
        official_url="https://example.com/",
        status=status,
    )


def make_course(game, title, slug, level=Course.Level.BEGINNER, status=Course.Status.PUBLISHED):
    return Course.objects.create(
        title=title,
        slug=slug,
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=level,
        description=f"Descripción de {title}.",
        requirements="Requisitos.",
        duration_weeks=2,
        price_cents=10000,
        access_days=30,
        status=status,
    )


@pytest.fixture
def catalog():
    first = make_game("Juego uno", "juego-uno")
    second = make_game("Juego dos", "juego-dos")
    hidden = make_game("Juego oculto", "juego-oculto", Game.Status.HIDDEN)
    courses = {
        "primero": make_course(first, "Curso de uno", "curso-de-uno"),
        "segundo": make_course(
            second, "Curso de dos", "curso-de-dos", level=Course.Level.INTERMEDIATE
        ),
        "borrador": make_course(
            first, "Curso en borrador", "curso-en-borrador", status=Course.Status.DRAFT
        ),
        "oculto": make_course(hidden, "Curso de juego oculto", "curso-de-juego-oculto"),
    }
    return {"juego-uno": first, "juego-dos": second, "cursos": courses}


def content(client, **params):
    response = client.get(reverse("courses:course_list"), params)
    assert response.status_code == 200
    return response.content.decode()


def test_url_del_listado_es_en_espanol():
    assert reverse("courses:course_list") == "/cursos/"


def test_sin_filtros_muestra_solo_publicados_de_juegos_activos(client, catalog):
    html = content(client)

    assert "Curso de uno" in html
    assert "Curso de dos" in html
    assert "Curso en borrador" not in html
    assert "Curso de juego oculto" not in html


def test_filtra_por_juego(client, catalog):
    html = content(client, juego="juego-uno")

    assert "Curso de uno" in html
    assert "Curso de dos" not in html


def test_filtra_por_nivel(client, catalog):
    html = content(client, nivel=Course.Level.INTERMEDIATE)

    assert "Curso de dos" in html
    assert "Curso de uno" not in html


def test_combina_juego_y_nivel(client, catalog):
    html = content(client, juego="juego-dos", nivel=Course.Level.BEGINNER)

    assert "Curso de dos" not in html
    assert "No hay cursos publicados con ese filtro." in html


def test_el_filtro_se_refleja_en_la_url(client, catalog):
    html = content(client, juego="juego-uno", nivel=Course.Level.BEGINNER)

    assert 'value="juego-uno" selected' in html
    assert 'value="beginner" selected' in html


def test_un_juego_inexistente_no_muestra_cursos(client, catalog):
    html = content(client, juego="no-existe")

    assert "Curso de uno" not in html
    assert "Curso de dos" not in html
    assert "No hay cursos publicados con ese filtro." in html


def test_un_nivel_invalido_no_filtra(client, catalog):
    html = content(client, nivel="avanzado")

    assert "Curso de uno" in html
    assert "Curso de dos" in html
