"""Recursos de una lección (EM-023)."""

from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonResource, Module
from enrollments.models import Enrollment

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
def lesson(module):
    return Lesson.objects.create(
        module=module,
        title="Lección uno",
        content="Cuerpo",
        estimated_minutes=10,
        order=1,
        status=Lesson.Status.PUBLISHED,
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


@pytest.fixture
def resource(lesson, version, environment):
    return LessonResource.objects.create(
        lesson=lesson,
        title="Repositorio base",
        url="https://example.com/plantilla",
        game_version=version,
        modding_environment=environment,
    )


def make_user(email, **extra):
    return get_user_model().objects.create_user(email=email, password="x-12345678", **extra)


def url(lesson):
    return reverse("courses:lesson_detail", args=[lesson.module.course.slug, lesson.pk])


def test_alumno_inscrito_ve_el_recurso_con_su_version_y_entorno(client, course, lesson, resource):
    user = make_user("alumno@example.com")
    Enrollment.objects.create(user=user, course=course, origin=Enrollment.Origin.SCHOLARSHIP)
    client.force_login(user)

    html = client.get(url(lesson)).content.decode()

    assert "Repositorio base" in html
    assert "https://example.com/plantilla" in html
    assert "Juego de prueba 1.4 + Loader 2.1" in html


def test_alumno_sin_inscripcion_no_ve_el_recurso(client, lesson, resource):
    client.force_login(make_user("sin-acceso@example.com"))

    assert client.get(url(lesson)).status_code == 403


def test_inscripcion_vencida_no_ve_el_recurso(client, course, lesson, resource):
    user = make_user("vencido@example.com")
    Enrollment.objects.create(
        user=user,
        course=course,
        origin=Enrollment.Origin.SCHOLARSHIP,
        access_ends_at=timezone.now() - timedelta(days=1),
    )
    client.force_login(user)

    assert client.get(url(lesson)).status_code == 403


def test_tutor_sin_inscripcion_ve_la_leccion_pero_no_los_recursos(client, lesson, resource):
    client.force_login(make_user("tutor@example.com", is_tutor=True))

    response = client.get(url(lesson))

    assert response.status_code == 200
    assert "Repositorio base" not in response.content.decode()


def test_leccion_de_muestra_muestra_los_recursos_sin_cuenta(client, lesson, resource):
    lesson.is_sample = True
    lesson.save(update_fields=["is_sample"])

    html = client.get(url(lesson)).content.decode()

    assert "Repositorio base" in html


def test_leccion_normal_no_muestra_los_recursos_sin_cuenta(client, lesson, resource):
    response = client.get(url(lesson))

    assert response.status_code == 302
    assert "Repositorio base" not in response.content.decode()


def test_no_acepta_version_de_otro_juego(lesson, environment):
    other_game = Game.objects.create(
        name="Otro juego",
        slug="otro-juego",
        description="Otro.",
        official_url="https://example.com/",
    )
    other_version = GameVersion.objects.create(
        game=other_game, number="9.9", release_date=date(2026, 1, 1)
    )

    with pytest.raises(ValidationError) as error:
        LessonResource(
            lesson=lesson,
            title="Ajeno",
            url="https://example.com/ajeno",
            game_version=other_version,
            modding_environment=environment,
        ).full_clean()

    assert "game_version" in error.value.message_dict


def test_no_acepta_entorno_de_otro_juego(lesson, version):
    other_game = Game.objects.create(
        name="Otro juego",
        slug="otro-juego",
        description="Otro.",
        official_url="https://example.com/",
    )
    other_environment = ModdingEnvironment.objects.create(
        game=other_game, name="Otro loader", version="1.0"
    )

    with pytest.raises(ValidationError) as error:
        LessonResource(
            lesson=lesson,
            title="Ajeno",
            url="https://example.com/ajeno",
            game_version=version,
            modding_environment=other_environment,
        ).full_clean()

    assert "modding_environment" in error.value.message_dict
