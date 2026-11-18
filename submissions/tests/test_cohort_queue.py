"""Las entregas de un grupo y su visibilidad para el tutor (EM-050)."""

from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from cohorts.models import Cohort
from courses.models import Course, Exercise, Lesson, Module
from enrollments.models import Enrollment
from submissions.models import Submission, SubmissionAttempt

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego",
        slug="juego",
        description="Un juego.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def course(game):
    return Course.objects.create(
        title="Curso por grupos",
        slug="curso-por-grupos",
        game=game,
        kind=Course.Kind.COURSE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=6,
        price_cents=19900,
        access_days=10,
        status=Course.Status.PUBLISHED,
    )


@pytest.fixture
def version(game):
    return GameVersion.objects.create(game=game, number="1.2", release_date=date(2026, 10, 1))


@pytest.fixture
def environment(game):
    return ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9")


@pytest.fixture
def lesson(course):
    module = Module.objects.create(course=course, title="Semana 1", order=1)
    return Lesson.objects.create(
        module=module,
        title="Lección uno",
        content="Cuerpo",
        estimated_minutes=10,
        order=1,
        status=Lesson.Status.PUBLISHED,
    )


@pytest.fixture
def exercise(lesson):
    return Exercise.objects.create(lesson=lesson, title="Tu primer mod", instructions="Hazlo.")


def make_user(email, tutor=False):
    user = get_user_model().objects.create_user(
        email=email, password="x-12345678", display_name=email.split("@")[0]
    )
    if tutor:
        user.is_tutor = True
        user.save(update_fields=["is_tutor"])
    return user


def make_submission(student, course, cohort, exercise, version, environment):
    enrollment = Enrollment.objects.create(
        user=student,
        course=course,
        cohort=cohort,
        origin=Enrollment.Origin.STRIPE,
        access_ends_at=timezone.now().replace(year=2027),
    )
    submission = Submission.objects.create(exercise=exercise, enrollment=enrollment)
    SubmissionAttempt.objects.create(
        submission=submission,
        repository_url="https://github.com/ana/mi-mod",
        game_version=version,
        modding_environment=environment,
    )
    return submission


@pytest.fixture
def cohort_a(course):
    tutor = make_user("tutora@example.com", tutor=True)
    cohort = Cohort.objects.create(
        course=course,
        name="Grupo A",
        start_date=date(2026, 11, 1),
        end_date=date(2026, 12, 1),
        capacity=8,
    )
    cohort.tutors.add(tutor)
    return cohort


@pytest.fixture
def cohort_b(course):
    tutor = make_user("tutorb@example.com", tutor=True)
    cohort = Cohort.objects.create(
        course=course,
        name="Grupo B",
        start_date=date(2026, 11, 1),
        end_date=date(2026, 12, 1),
        capacity=8,
    )
    cohort.tutors.add(tutor)
    return cohort


def test_cada_tutor_ve_solo_las_entregas_de_sus_grupos(
    client, course, cohort_a, cohort_b, exercise, version, environment
):
    make_submission(
        make_user("alumna@example.com"), course, cohort_a, exercise, version, environment
    )
    make_submission(
        make_user("alumnob@example.com"), course, cohort_b, exercise, version, environment
    )
    client.force_login(cohort_a.tutors.get())

    html = client.get(reverse("reviews:queue")).content.decode()

    assert "alumna@example.com" in html
    assert "alumnob@example.com" not in html
    assert "Grupo A" in html


def test_el_alumno_ve_el_grupo_en_su_entrega(
    client, course, cohort_a, exercise, lesson, version, environment
):
    student = make_user("alumna@example.com")
    enrollment = Enrollment.objects.create(
        user=student,
        course=course,
        cohort=cohort_a,
        origin=Enrollment.Origin.STRIPE,
        access_ends_at=timezone.now().replace(year=2027),
    )
    client.force_login(student)

    html = client.get(reverse("submissions:submit", args=[lesson.pk])).content.decode()

    assert "Grupo A" in html
    assert enrollment.cohort == cohort_a
