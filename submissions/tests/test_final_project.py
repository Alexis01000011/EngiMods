"""Proyecto final con checklist de publicación (EM-076)."""

from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, Module
from enrollments.models import Enrollment
from submissions.models import PublicationChecklist, Submission, SubmissionAttempt

pytestmark = pytest.mark.django_db

REPO = "https://github.com/ana/mi-mod-final"
PUBLISHED = "https://mods.example.com/mi-mod"


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
def version(game):
    return GameVersion.objects.create(game=game, number="1.2", release_date=date(2026, 10, 1))


@pytest.fixture
def environment(game):
    return ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9")


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
def lesson(course):
    module = Module.objects.create(course=course, title="Semana 1", order=1)
    return Lesson.objects.create(
        module=module,
        title="Lección final",
        content="Cuerpo",
        estimated_minutes=10,
        order=1,
        status=Lesson.Status.PUBLISHED,
    )


@pytest.fixture
def exercise(lesson):
    return Exercise.objects.create(
        lesson=lesson,
        title="Proyecto final",
        instructions="Publica tu mod.",
        is_final_project=True,
    )


@pytest.fixture
def student():
    return get_user_model().objects.create_user(
        email="alumno@example.com", password="x-12345678", display_name="Alumno"
    )


@pytest.fixture
def enrollment(student, course):
    now = timezone.now()
    return Enrollment.objects.create(
        user=student,
        course=course,
        origin=Enrollment.Origin.TRIAL,
        enrolled_at=now - timedelta(days=10),
        access_ends_at=now + timedelta(days=20),
    )


def submit_url(lesson):
    return reverse("submissions:submit", args=[lesson.pk])


def form_data(version, environment, **overrides):
    data = {
        "repository_url": REPO,
        "game_version": version.pk,
        "modding_environment": environment.pk,
        "comment": "Listo para publicar.",
        "readme": "on",
        "license": "on",
        "changelog": "on",
        "publication_url": PUBLISHED,
    }
    data.update(overrides)
    return data


def make_submission(enrollment, exercise, version, environment, status=Submission.Status.SUBMITTED):
    submission = Submission.objects.create(exercise=exercise, enrollment=enrollment, status=status)
    attempt = SubmissionAttempt.objects.create(
        submission=submission,
        repository_url=REPO,
        game_version=version,
        modding_environment=environment,
    )
    PublicationChecklist.objects.create(
        attempt=attempt, readme=True, license=True, changelog=True, publication_url=PUBLISHED
    )
    return submission, attempt


def test_el_proyecto_final_pide_el_checklist(client, student, enrollment, exercise, lesson):
    client.force_login(student)

    html = client.get(submit_url(lesson)).content.decode()

    assert "Checklist de publicación" in html
    for field in ("readme", "license", "changelog", "publication_url"):
        assert f'name="{field}"' in html


def test_un_ejercicio_normal_no_pide_el_checklist(client, student, enrollment, exercise, lesson):
    exercise.is_final_project = False
    exercise.save(update_fields=["is_final_project"])
    client.force_login(student)

    html = client.get(submit_url(lesson)).content.decode()

    assert "Checklist de publicación" not in html
    assert 'name="readme"' not in html


def test_no_se_entrega_el_proyecto_final_sin_el_checklist(
    client, student, enrollment, exercise, lesson, version, environment
):
    client.force_login(student)

    response = client.post(
        submit_url(lesson),
        form_data(version, environment, readme="", license="", changelog=""),
    )

    assert response.status_code == 200
    assert not Submission.objects.exists()
    assert not PublicationChecklist.objects.exists()


def test_entrega_el_proyecto_final_con_checklist_y_publicacion(
    client, student, enrollment, exercise, lesson, version, environment
):
    client.force_login(student)

    response = client.post(submit_url(lesson), form_data(version, environment))

    assert response.status_code == 302
    checklist = PublicationChecklist.objects.get()
    assert checklist.readme and checklist.license and checklist.changelog
    assert checklist.publication_url == PUBLISHED
    assert checklist.attempt.game_version == version


def test_la_publicacion_es_opcional(
    client, student, enrollment, exercise, lesson, version, environment
):
    client.force_login(student)

    response = client.post(submit_url(lesson), form_data(version, environment, publication_url=""))

    assert response.status_code == 302
    assert PublicationChecklist.objects.get().publication_url == ""


def test_el_reenvio_guarda_un_checklist_nuevo(
    client, student, enrollment, exercise, lesson, version, environment
):
    submission, first_attempt = make_submission(
        enrollment, exercise, version, environment, status=Submission.Status.CHANGES_REQUESTED
    )
    client.force_login(student)

    response = client.post(
        submit_url(lesson),
        form_data(version, environment, repository_url="https://github.com/ana/mi-mod-v2"),
    )

    assert response.status_code == 302
    assert submission.attempts.count() == 2
    assert PublicationChecklist.objects.count() == 2
    new_attempt = submission.attempts.exclude(pk=first_attempt.pk).get()
    assert new_attempt.publication_checklist.publication_url == PUBLISHED


def test_el_tutor_ve_el_checklist_al_revisar(
    client, student, enrollment, exercise, version, environment
):
    submission, _attempt = make_submission(enrollment, exercise, version, environment)
    tutor = get_user_model().objects.create_user(
        email="tutor@example.com", password="x-12345678", is_tutor=True
    )
    client.force_login(tutor)

    html = client.get(reverse("reviews:review", args=[submission.pk])).content.decode()

    assert "Checklist de publicación" in html
    assert "README" in html
    assert "Licencia" in html
    assert "Registro de cambios" in html
    assert PUBLISHED in html
