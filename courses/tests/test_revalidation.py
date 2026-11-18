"""Revalidación de lecciones al salir una versión nueva (EM-014)."""

from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonTest, Module
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
def old_version(game):
    return GameVersion.objects.create(
        game=game, number="1.0", release_date=date(2025, 1, 1), is_current=True
    )


@pytest.fixture
def environment(game, old_version):
    environment = ModdingEnvironment.objects.create(game=game, name="Loader", version="1.0")
    environment.compatible_versions.add(old_version)
    return environment


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
def tested_lesson(module, old_version, environment):
    lesson = Lesson.objects.create(
        module=module,
        title="Lección probada",
        content="Cuerpo",
        estimated_minutes=10,
        order=1,
        status=Lesson.Status.PUBLISHED,
    )
    LessonTest.objects.create(
        lesson=lesson,
        game_version=old_version,
        modding_environment=environment,
        tested_on=date(2025, 2, 1),
    )
    return lesson


@pytest.fixture
def current_version(game, old_version, environment):
    old_version.is_current = False
    old_version.save(update_fields=["is_current"])
    version = GameVersion.objects.create(
        game=game, number="2.0", release_date=date(2026, 10, 1), is_current=True
    )
    environment.compatible_versions.add(version)
    return version


def make_user(email, tutor=False):
    user = get_user_model().objects.create_user(
        email=email, password="x-12345678", display_name=email.split("@")[0]
    )
    if tutor:
        user.is_tutor = True
        user.save(update_fields=["is_tutor"])
    return user


def lesson_url(lesson):
    return reverse("courses:lesson_detail", args=[lesson.module.course.slug, lesson.pk])


def test_una_leccion_con_la_version_actual_no_esta_pendiente(client, tested_lesson, course):
    student = make_user("alumno@example.com")
    Enrollment.objects.create(user=student, course=course, origin=Enrollment.Origin.TRIAL)
    client.force_login(student)

    html = client.get(lesson_url(tested_lesson)).content.decode()

    assert "Pendiente de revalidar" not in html


def test_el_alumno_ve_probado_en_la_anterior_y_pendiente_en_la_actual(
    client, tested_lesson, current_version, course
):
    student = make_user("alumno@example.com")
    Enrollment.objects.create(user=student, course=course, origin=Enrollment.Origin.TRIAL)
    client.force_login(student)

    html = client.get(lesson_url(tested_lesson)).content.decode()

    assert "Probado en 1.0. Pendiente de revalidar en 2.0." in html


def test_la_cola_es_solo_para_tutores(client, tested_lesson, current_version):
    client.force_login(make_user("alumno@example.com"))
    assert client.get(reverse("revalidation:queue")).status_code == 403


def test_la_cola_muestra_solo_lecciones_pendientes_por_curso(
    client, tested_lesson, current_version, module
):
    up_to_date = Lesson.objects.create(
        module=module,
        title="Lección al día",
        content="Cuerpo",
        estimated_minutes=10,
        order=2,
        status=Lesson.Status.PUBLISHED,
    )
    LessonTest.objects.create(
        lesson=up_to_date,
        game_version=current_version,
        modding_environment=tested_lesson.tests.get().modding_environment,
        tested_on=date(2026, 11, 1),
    )
    Lesson.objects.create(
        module=module,
        title="Lección sin pruebas",
        content="Cuerpo",
        estimated_minutes=10,
        order=3,
        status=Lesson.Status.PUBLISHED,
    )
    client.force_login(make_user("tutor@example.com", tutor=True))

    html = client.get(reverse("revalidation:queue")).content.decode()

    assert "Curso de prueba" in html
    assert "Lección probada" in html
    assert "Lección al día" not in html
    assert "Lección sin pruebas" not in html
    assert "Pendiente de revalidar en 2.0" in html


def test_el_tutor_registra_la_nueva_version_y_la_fecha(
    client, tested_lesson, current_version, environment, course
):
    tutor = make_user("tutor@example.com", tutor=True)
    client.force_login(tutor)

    response = client.post(
        reverse("revalidation:revalidate", args=[tested_lesson.pk]),
        {
            "game_version": current_version.pk,
            "modding_environment": environment.pk,
            "tested_on": "2026-11-18",
        },
    )

    assert response.status_code == 302
    test = tested_lesson.tests.get(game_version=current_version)
    assert test.tested_on == date(2026, 11, 18)
    queue_html = client.get(reverse("revalidation:queue")).content.decode()
    assert "No hay lecciones pendientes de revalidar." in queue_html


def test_despues_de_revalidar_el_alumno_ya_no_ve_el_aviso(
    client, tested_lesson, current_version, environment, course
):
    tutor = make_user("tutor@example.com", tutor=True)
    student = make_user("alumno@example.com")
    Enrollment.objects.create(user=student, course=course, origin=Enrollment.Origin.TRIAL)
    client.force_login(tutor)
    client.post(
        reverse("revalidation:revalidate", args=[tested_lesson.pk]),
        {
            "game_version": current_version.pk,
            "modding_environment": environment.pk,
            "tested_on": "2026-11-18",
        },
    )
    client.force_login(student)

    html = client.get(lesson_url(tested_lesson)).content.decode()

    assert "Pendiente de revalidar" not in html
    assert "Probado con" in html


def test_no_acepta_version_de_otro_juego(client, tested_lesson, current_version):
    other_game = Game.objects.create(
        name="Otro", slug="otro", description="Otro.", official_url="https://example.com/"
    )
    other_version = GameVersion.objects.create(
        game=other_game, number="9.9", release_date=date(2026, 1, 1)
    )
    other_environment = ModdingEnvironment.objects.create(
        game=other_game, name="Otro loader", version="1.0"
    )
    client.force_login(make_user("tutor@example.com", tutor=True))

    response = client.post(
        reverse("revalidation:revalidate", args=[tested_lesson.pk]),
        {
            "game_version": other_version.pk,
            "modding_environment": other_environment.pk,
            "tested_on": "2026-11-18",
        },
    )

    assert response.status_code == 302
    assert not tested_lesson.tests.filter(game_version=other_version).exists()
    assert tested_lesson.tests.count() == 1
