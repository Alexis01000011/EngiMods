"""Landing de EngiMods (EM-040)."""

from datetime import date

import pytest
from django.urls import reverse

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonTest, Module

pytestmark = pytest.mark.django_db


def make_game(name="Juego de prueba", slug="juego-de-prueba", status=Game.Status.ACTIVE):
    return Game.objects.create(
        name=name,
        slug=slug,
        description=f"Descripción de {name}.",
        official_url="https://example.com/",
        status=status,
    )


def make_course(game, title, slug, kind=Course.Kind.SHORT_PRACTICE, status=None):
    return Course.objects.create(
        title=title,
        slug=slug,
        game=game,
        kind=kind,
        level=Course.Level.BEGINNER,
        description="Construye tu primer mod.",
        requirements="Programación básica.",
        duration_weeks=2,
        price_cents=19900,
        access_days=30,
        status=status or Course.Status.PUBLISHED,
    )


def record_test(course, game, number, tested_on, lesson_status=Lesson.Status.PUBLISHED):
    module, _ = Module.objects.get_or_create(course=course, title="Módulo 1", order=1)
    lesson = Lesson.objects.create(
        module=module,
        title=f"Lección {number}",
        content="Texto.",
        estimated_minutes=10,
        order=Lesson.objects.filter(module=module).count() + 1,
        status=lesson_status,
    )
    version, _ = GameVersion.objects.get_or_create(
        game=game, number=number, defaults={"release_date": date(2026, 1, 1)}
    )
    environment, _ = ModdingEnvironment.objects.get_or_create(
        game=game, name="Loader X", version="0.9"
    )
    LessonTest.objects.create(
        lesson=lesson, game_version=version, modding_environment=environment, tested_on=tested_on
    )


def home(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    return response.content.decode()


def test_cualquier_visitante_ve_la_landing_sin_cuenta(client):
    html = home(client)
    assert "Aprende a crear mods como se construye el software" in html


def test_presenta_la_propuesta_de_valor(client):
    html = home(client)
    for point in (
        "Una ruta en español",
        "Ejercicios pequeños",
        "Versión comprobada",
        "Revisión de lo que construyes",
    ):
        assert point in html


def test_el_plazo_de_revision_sale_de_settings(client, settings):
    settings.REVIEW_DEADLINE_HOURS = 48
    assert "en menos de 48 horas" in home(client)


def test_muestra_juegos_activos_y_no_los_ocultos(client):
    make_game("Juego visible", "juego-visible")
    make_game("Juego oculto", "juego-oculto", status=Game.Status.HIDDEN)
    html = home(client)
    assert "Juego visible" in html
    assert "Juego oculto" not in html


def test_cada_juego_enlaza_a_su_pagina(client):
    game = make_game()
    assert f'href="{game.get_absolute_url()}"' in home(client)


def test_el_juego_muestra_su_version_actual_y_sus_cursos_publicados(client):
    game = make_game()
    GameVersion.objects.create(game=game, number="1.4", release_date=date(2026, 1, 1))
    GameVersion.objects.filter(number="1.4").update(is_current=True)
    make_course(game, "Publicado", "publicado")
    make_course(game, "Borrador", "borrador", status=Course.Status.DRAFT)
    html = home(client)
    assert "Versión actual: 1.4" in html
    assert "1 curso<" in html


def test_muestra_cursos_publicados_y_no_borradores(client):
    game = make_game()
    published = make_course(game, "Misión Cero de prueba", "mision-cero")
    make_course(game, "Curso en borrador", "curso-borrador", status=Course.Status.DRAFT)
    html = home(client)
    assert "Misión Cero de prueba" in html
    assert reverse("courses:course_detail", args=[published.slug]) in html
    assert "Curso en borrador" not in html
    assert "MXN 199.00" in html


def test_sin_cursos_publicados_lo_dice(client):
    html = home(client)
    assert "Aún no hay cursos publicados" in html
    assert "button-primary" not in html


def test_con_una_practica_el_llamado_lleva_a_su_pagina(client):
    practice = make_course(make_game(), "Misión Cero", "mision-cero")
    html = home(client)
    url = reverse("courses:course_detail", args=[practice.slug])
    assert f'<a href="{url}" class="button-primary">Empieza con Misión Cero</a>' in html


def test_con_varias_practicas_el_llamado_lleva_a_la_lista(client):
    game = make_game()
    make_course(game, "Misión Cero A", "mision-cero-a")
    make_course(game, "Misión Cero B", "mision-cero-b")
    assert '<a href="#cursos" class="button-primary">Elige tu práctica para empezar</a>' in (
        home(client)
    )


def test_llamado_al_grupo_piloto_cuando_hay_un_curso_por_grupos(client):
    group = make_course(make_game(), "Curso de seis semanas", "curso", kind=Course.Kind.COURSE)
    html = home(client)
    url = reverse("courses:course_detail", args=[group.slug])
    assert f'<a href="{url}" class="button-secondary">Conoce el grupo piloto</a>' in html
    assert "todavía no abre inscripciones" not in html


def test_sin_curso_por_grupos_avisa_que_el_piloto_no_abre(client):
    make_course(make_game(), "Misión Cero", "mision-cero")
    html = home(client)
    assert "Conoce el grupo piloto" not in html
    assert "El grupo piloto todavía no abre inscripciones." in html


def test_el_curso_muestra_su_prueba_mas_reciente_publicada(client):
    game = make_game()
    course = make_course(game, "Misión Cero", "mision-cero")
    record_test(course, game, "1.3", date(2026, 10, 1))
    record_test(course, game, "1.4", date(2026, 11, 1))
    record_test(course, game, "1.5", date(2026, 11, 3), lesson_status=Lesson.Status.DRAFT)
    html = home(client)
    assert "Probado con Juego de prueba 1.4 + Loader X 0.9" in html
    assert "1.5 +" not in html


def test_un_curso_sin_pruebas_lo_dice_con_palabras(client):
    make_course(make_game(), "Misión Cero", "mision-cero")
    assert "Sin versión probada" in home(client)


def test_la_landing_se_adapta_al_telefono(client):
    make_course(make_game(), "Misión Cero", "mision-cero")
    html = home(client)
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html
    # Una columna en teléfono; la rejilla crece solo en pantallas anchas.
    assert "grid-cols-1" in html
    assert "md:grid-cols-2" in html


def test_las_practicas_cortas_van_antes_que_los_cursos(client):
    game = make_game()
    make_course(game, "Aaa curso por grupos", "aaa", kind=Course.Kind.COURSE)
    make_course(game, "Zzz práctica", "zzz")
    html = home(client)
    assert html.index("Zzz práctica</h3>") < html.index("Aaa curso por grupos</h3>")
