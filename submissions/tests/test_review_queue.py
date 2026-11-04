from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, Module
from enrollments.models import Enrollment
from submissions.models import Submission, SubmissionAttempt

pytestmark = pytest.mark.django_db

QUEUE = "/tutoria/entregas/"


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
        title="Misión Cero",
        slug="mision-cero",
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
def version(game):
    return GameVersion.objects.create(game=game, number="1.2", release_date=date(2026, 10, 1))


@pytest.fixture
def environment(game):
    return ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9")


@pytest.fixture
def module(course):
    return Module.objects.create(course=course, title="Semana 1", order=1)


def make_exercise(module, title, order):
    lesson = Lesson.objects.create(
        module=module,
        title=f"Lección {title}",
        content="Cuerpo",
        estimated_minutes=10,
        order=order,
        status=Lesson.Status.PUBLISHED,
    )
    return Exercise.objects.create(lesson=lesson, title=title, instructions="Haz algo.")


def make_user(email, tutor=False, **kwargs):
    user = get_user_model().objects.create_user(email=email, password="x-12345678", **kwargs)
    if tutor:
        user.is_tutor = True
        user.save()
    return user


@pytest.fixture
def tutor():
    return make_user("tutor@example.com", tutor=True)


@pytest.fixture
def enrollment(course):
    return Enrollment.objects.create(
        user=make_user("alumno@example.com"), course=course, origin=Enrollment.Origin.TRIAL
    )


@pytest.fixture
def make_submission(enrollment, module, version, environment):
    count = {"n": 0}

    def make(title="Ejercicio", hours_ago=1, status=Submission.Status.SUBMITTED):
        count["n"] += 1
        exercise = make_exercise(module, title, count["n"])
        submission = Submission.objects.create(
            exercise=exercise, enrollment=enrollment, status=status
        )
        SubmissionAttempt.objects.create(
            submission=submission,
            repository_url="https://github.com/ana/mi-mod",
            game_version=version,
            modding_environment=environment,
            submitted_at=timezone.now() - timedelta(hours=hours_ago),
        )
        return submission

    return make


def review_url(submission):
    return reverse("reviews:review", args=[submission.pk])


def start_url(submission):
    return reverse("reviews:start_review", args=[submission.pk])


def test_urls_are_in_spanish(make_submission):
    submission = make_submission()
    assert reverse("reviews:queue") == QUEUE
    assert review_url(submission) == f"/tutoria/entregas/{submission.pk}/"
    assert start_url(submission) == f"/tutoria/entregas/{submission.pk}/tomar/"


# Pantalla propia del tutor con las pendientes, de la más vieja a la más nueva


def test_queue_lists_pending_oldest_first(client, tutor, make_submission):
    make_submission("Reciente", hours_ago=1)
    make_submission("Antigua", hours_ago=10)
    make_submission("Media", hours_ago=5)
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert content.index("Antigua") < content.index("Media") < content.index("Reciente")


def test_queue_includes_in_review_and_excludes_reviewed(client, tutor, make_submission):
    make_submission("Pendiente", status=Submission.Status.SUBMITTED)
    make_submission("Tomada", status=Submission.Status.IN_REVIEW)
    make_submission("Aprobada", status=Submission.Status.APPROVED)
    make_submission("Con cambios", status=Submission.Status.CHANGES_REQUESTED)
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert "Pendiente" in content
    assert "Tomada" in content
    assert ">Aprobada<" not in content
    assert "Con cambios" not in content


def test_queue_empty(client, tutor):
    client.force_login(tutor)
    assert "No hay entregas pendientes." in client.get(QUEUE).content.decode()


def test_queue_shows_student_and_course(client, tutor, make_submission):
    make_submission()
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert "alumno@example.com" in content
    assert "Misión Cero" in content


# Mientras no haya grupos, todos los tutores ven todas las entregas


def test_every_tutor_sees_every_submission(client, make_submission):
    make_submission("Del alumno")
    for email in ("uno@example.com", "dos@example.com"):
        client.force_login(make_user(email, tutor=True))
        assert "Del alumno" in client.get(QUEUE).content.decode()


def test_superuser_can_see_queue(client, make_submission):
    make_submission("Del alumno")
    admin = get_user_model().objects.create_superuser(email="admin@example.com", password="x-1")
    client.force_login(admin)
    assert client.get(QUEUE).status_code == 200


@pytest.mark.parametrize("url_name", ["queue", "review", "start_review"])
def test_anonymous_is_forbidden(client, make_submission, url_name):
    submission = make_submission()
    args = [] if url_name == "queue" else [submission.pk]
    url = reverse(f"reviews:{url_name}", args=args)
    response = client.post(url) if url_name == "start_review" else client.get(url)
    assert response.status_code == 403


@pytest.mark.parametrize("kwargs", [{}, {"is_staff": True}], ids=["alumno", "staff-sin-tutor"])
def test_non_tutor_is_forbidden(client, make_submission, enrollment, kwargs):
    submission = make_submission()
    client.force_login(make_user("no-tutor@example.com", **kwargs))
    assert client.get(QUEUE).status_code == 403
    assert client.get(review_url(submission)).status_code == 403
    assert client.post(start_url(submission)).status_code == 403
    submission.refresh_from_db()
    assert submission.status == Submission.Status.SUBMITTED


def test_student_cannot_open_own_submission_review(client, enrollment, make_submission):
    submission = make_submission()
    client.force_login(enrollment.user)
    assert client.post(start_url(submission)).status_code == 403


def test_inactive_tutor_is_forbidden(client, make_submission):
    tutor = make_user("inactivo@example.com", tutor=True)
    tutor.is_active = False
    tutor.save()
    client.force_login(tutor)
    assert client.get(QUEUE).status_code == 403


# Las que pasan del plazo se marcan en rojo; el plazo es un setting


def test_overdue_submissions_are_marked(client, tutor, make_submission):
    make_submission("Atrasada", hours_ago=25)
    make_submission("A tiempo", hours_ago=23)
    client.force_login(tutor)
    response = client.get(QUEUE)
    flags = {item.exercise.title: item.overdue for item in response.context["submissions"]}
    assert flags == {"Atrasada": True, "A tiempo": False}
    content = response.content.decode()
    assert content.count("Fuera de plazo") == 1
    assert content.count("bg-error-container") == 1
    assert "Plazo de revisión: 24 horas." in content


@override_settings(REVIEW_DEADLINE_HOURS=2)
def test_deadline_comes_from_settings(client, tutor, make_submission):
    make_submission("Tres horas", hours_ago=3)
    client.force_login(tutor)
    response = client.get(QUEUE)
    assert response.context["submissions"][0].overdue is True
    assert "Plazo de revisión: 2 horas." in response.content.decode()


def test_in_review_submission_past_deadline_is_still_marked(client, tutor, make_submission):
    make_submission("Tomada tarde", hours_ago=30, status=Submission.Status.IN_REVIEW)
    client.force_login(tutor)
    assert client.get(QUEUE).context["submissions"][0].overdue is True


# Al abrir la revisión pasa a en revisión y la cola muestra qué tutor la tiene


def test_queue_offers_to_open_review(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert start_url(submission) in content
    assert "Sin tutor asignado." in content


def test_opening_review_sets_in_review_and_tutor(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    response = client.post(start_url(submission))
    assert response.status_code == 302
    assert response.url == review_url(submission)
    submission.refresh_from_db()
    attempt = submission.attempts.get()
    assert submission.status == Submission.Status.IN_REVIEW
    assert attempt.reviewer == tutor
    assert attempt.review_started_at is not None


def test_queue_shows_which_tutor_has_it(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    client.post(start_url(submission))
    client.force_login(make_user("otro-tutor@example.com", tutor=True))
    content = client.get(QUEUE).content.decode()
    assert "En revisión · la tiene tutor@example.com." in content
    assert start_url(submission) not in content


def test_second_tutor_does_not_take_over(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    client.post(start_url(submission))
    first_start = submission.attempts.get().review_started_at
    client.force_login(make_user("otro-tutor@example.com", tutor=True))
    client.post(start_url(submission))
    attempt = submission.attempts.get()
    assert attempt.reviewer == tutor
    assert attempt.review_started_at == first_start


def test_reviewed_submission_is_not_reopened(client, tutor, make_submission):
    submission = make_submission(status=Submission.Status.APPROVED)
    client.force_login(tutor)
    client.post(start_url(submission))
    submission.refresh_from_db()
    assert submission.status == Submission.Status.APPROVED
    assert submission.attempts.get().reviewer is None


def test_start_review_requires_post(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    assert client.get(start_url(submission)).status_code == 405
    submission.refresh_from_db()
    assert submission.status == Submission.Status.SUBMITTED


def test_viewing_review_page_does_not_take_it(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    response = client.get(review_url(submission))
    assert response.status_code == 200
    assert "Tomar la revisión" in response.content.decode()
    submission.refresh_from_db()
    assert submission.status == Submission.Status.SUBMITTED


def test_review_page_shows_submission_details(client, tutor, make_submission):
    submission = make_submission("Mi ejercicio")
    client.force_login(tutor)
    client.post(start_url(submission))
    content = client.get(review_url(submission)).content.decode()
    assert "Mi ejercicio" in content
    assert "https://github.com/ana/mi-mod" in content
    assert "1.2 + Loader 0.9" in content
    assert "tutor@example.com" in content
    assert "Tomar la revisión" not in content


def test_review_of_missing_submission_returns_404(client, tutor):
    client.force_login(tutor)
    assert client.get(reverse("reviews:review", args=[999])).status_code == 404
    assert client.post(reverse("reviews:start_review", args=[999])).status_code == 404


# Se registra la hora de envío y la hora de revisión


def test_send_and_review_times_are_recorded(client, tutor, make_submission):
    submission = make_submission(hours_ago=3)
    client.force_login(tutor)
    before = timezone.now()
    client.post(start_url(submission))
    attempt = submission.attempts.get()
    assert attempt.submitted_at < before
    assert before <= attempt.review_started_at <= timezone.now()


def test_queue_shows_send_time(client, tutor, make_submission):
    make_submission(hours_ago=3)
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert "Enviada el" in content
    assert "hace 3" in content


# Pantalla según DESIGN.md (EM-077)


def test_only_most_urgent_submission_has_primary_button(client, tutor, make_submission):
    make_submission("Reciente", hours_ago=1)
    make_submission("Antigua", hours_ago=10)
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert content.count('class="button-primary') == 1
    assert content.count('class="button-secondary') == 1
    # La más urgente es la más vieja, que va primero.
    assert content.index("button-primary") < content.index("Reciente")


def test_queue_shows_remaining_time_and_status(client, tutor, make_submission):
    make_submission("A tiempo", hours_ago=1)
    client.force_login(tutor)
    content = client.get(QUEUE).content.decode()
    assert "Quedan 22" in content
    assert "Estado: Enviada" in content


def test_review_page_has_one_primary_button_until_taken(client, tutor, make_submission):
    submission = make_submission()
    client.force_login(tutor)
    assert client.get(review_url(submission)).content.decode().count('class="button-primary') == 1
    client.post(start_url(submission))
    assert "button-primary" not in client.get(review_url(submission)).content.decode()
