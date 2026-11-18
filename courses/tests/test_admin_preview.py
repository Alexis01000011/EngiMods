"""Vista previa de lecciones desde el admin (EM-022)."""

from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, LessonResource, LessonTest, Module

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def course(game):
    return Course.objects.create(
        title="Curso de prueba",
        slug="curso-de-prueba",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )


@pytest.fixture
def module(course):
    return Module.objects.create(course=course, title="Semana 1", order=1)


@pytest.fixture
def draft(module):
    return Lesson.objects.create(
        module=module,
        title="Lección en borrador",
        content="## Paso 1\n\n<script>alert(1)</script>Contenido en borrador.",
        estimated_minutes=10,
        order=1,
        status=Lesson.Status.DRAFT,
    )


@pytest.fixture
def version(game):
    return GameVersion.objects.create(
        game=game, number="1.4", release_date=date(2026, 1, 1), is_current=True
    )


@pytest.fixture
def environment(game, version):
    environment = ModdingEnvironment.objects.create(game=game, name="Loader", version="2.1")
    environment.compatible_versions.add(version)
    return environment


def preview_url(lesson):
    return reverse("admin:courses_lesson_preview", args=[lesson.pk])


def test_el_admin_muestra_el_boton_de_vista_previa(admin_client, draft):
    response = admin_client.get(reverse("admin:courses_lesson_change", args=[draft.pk]))

    assert response.status_code == 200
    assert "Ver como alumno" in response.content.decode()
    assert preview_url(draft) in response.content.decode()


def test_la_vista_previa_renderiza_una_leccion_en_borrador(admin_client, draft):
    response = admin_client.get(preview_url(draft))

    assert response.status_code == 200
    html = response.content.decode()
    assert "Lección en borrador" in html
    assert "<h2>Paso 1</h2>" in html
    assert "Vista previa para el equipo" in html
    assert "<script" not in html


def test_la_vista_previa_muestra_version_recursos_y_ejercicio(
    admin_client, draft, version, environment
):
    LessonTest.objects.create(
        lesson=draft,
        game_version=version,
        modding_environment=environment,
        tested_on=date(2026, 1, 2),
    )
    LessonResource.objects.create(
        lesson=draft,
        title="Repositorio base",
        url="https://example.com/plantilla",
        game_version=version,
        modding_environment=environment,
    )
    Exercise.objects.create(lesson=draft, title="Tu primer mod", instructions="Sube tu mod.")

    html = admin_client.get(preview_url(draft)).content.decode()

    assert "Juego de prueba 1.4 + Loader 2.1" in html
    assert "Repositorio base" in html
    assert "Ejercicio: Tu primer mod" in html
    assert "Sube tu mod." in html


def test_un_usuario_sin_permiso_de_admin_no_entra(client, draft):
    user = get_user_model().objects.create_user(
        email="alumno@example.com", password="x-12345678", display_name="Alumno"
    )
    client.force_login(user)

    response = client.get(preview_url(draft))

    assert response.status_code == 302
    assert reverse("admin:login") in response.url


def test_la_vista_previa_de_una_leccion_inexistente_da_404(admin_client):
    response = admin_client.get(reverse("admin:courses_lesson_preview", args=[999999]))

    assert response.status_code == 404


def test_la_leccion_en_borrador_sigue_sin_ser_publica(admin_client, draft):
    response = admin_client.get(
        reverse("courses:lesson_detail", args=[draft.module.course.slug, draft.pk])
    )

    assert response.status_code == 404
