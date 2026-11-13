"""EM-073: reenviar una entrega después de que el tutor pidió cambios."""

from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, Module, RubricCriterion
from enrollments.models import Enrollment
from submissions.models import Review, ReviewScore, Submission, SubmissionAttempt

pytestmark = pytest.mark.django_db

FIRST_REPO = "https://github.com/ana/mi-mod"
NEW_REPO = "https://github.com/ana/mi-mod-v2"
FIRST_COMMENT = "Falta explicar en el README cómo se instala."


def make_user(email, tutor=False, **kwargs):
    user = get_user_model().objects.create_user(email=email, password="x-12345678", **kwargs)
    if tutor:
        user.is_tutor = True
        user.save()
    return user


def enroll(user, course, days_left=10):
    now = timezone.now()
    return Enrollment.objects.create(
        user=user,
        course=course,
        origin=Enrollment.Origin.TRIAL,
        enrolled_at=now - timedelta(days=30),
        access_ends_at=now + timedelta(days=days_left),
    )


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
def new_version(game):
    return GameVersion.objects.create(game=game, number="1.3", release_date=date(2026, 11, 1))


@pytest.fixture
def environment(game):
    return ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9")


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
def lesson(course):
    module = Module.objects.create(course=course, title="Semana 1", order=1)
    return Lesson.objects.create(
        module=module,
        title="Tu primer mod",
        content="Cuerpo",
        estimated_minutes=10,
        order=1,
        status=Lesson.Status.PUBLISHED,
    )


@pytest.fixture
def exercise(lesson):
    return Exercise.objects.create(lesson=lesson, title="Ejercicio uno", instructions="Haz algo.")


@pytest.fixture
def criterion(exercise):
    return RubricCriterion.objects.create(exercise=exercise, title="Uso de Git", order=1)


@pytest.fixture
def student():
    return make_user("alumno@example.com", display_name="Ana")


@pytest.fixture
def tutor():
    return make_user("tutor@example.com", tutor=True, display_name="Luis")


@pytest.fixture
def enrollment(student, course):
    return enroll(student, course)


def make_submission(enrollment, exercise, version, environment, hours_ago=30, **kwargs):
    submission = Submission.objects.create(exercise=exercise, enrollment=enrollment, **kwargs)
    SubmissionAttempt.objects.create(
        submission=submission,
        repository_url=FIRST_REPO,
        game_version=version,
        modding_environment=environment,
        comment="Primer intento.",
        submitted_at=timezone.now() - timedelta(hours=hours_ago),
    )
    return submission


def request_changes(submission, tutor, criterion, comment=FIRST_COMMENT):
    """El tutor tomó el envío más reciente y pidió cambios, como en EM-072."""
    attempt = submission.attempts.order_by("-submitted_at", "-pk").first()
    attempt.reviewer = tutor
    attempt.review_started_at = timezone.now()
    attempt.save()
    review = Review.objects.create(
        attempt=attempt,
        reviewer=tutor,
        decision=Review.Decision.CHANGES_REQUESTED,
        comment=comment,
    )
    ReviewScore.objects.create(review=review, criterion=criterion, level=ReviewScore.Level.PARTIAL)
    submission.status = Submission.Status.CHANGES_REQUESTED
    submission.save()
    return review


@pytest.fixture
def changes_requested(enrollment, exercise, version, environment, tutor, criterion):
    submission = make_submission(enrollment, exercise, version, environment)
    request_changes(submission, tutor, criterion)
    return submission


def submit_url(lesson):
    return reverse("submissions:submit", args=[lesson.pk])


def resubmit_data(version, environment, **overrides):
    data = {
        "repository_url": NEW_REPO,
        "game_version": version.pk,
        "modding_environment": environment.pk,
        "comment": "Ya agregué la instalación al README.",
    }
    data.update(overrides)
    return data


# El alumno puede reenviar después de recibir cambios


def test_student_sees_resubmit_form_after_changes(
    client, student, changes_requested, lesson, version
):
    client.force_login(student)
    content = client.get(submit_url(lesson)).content.decode()
    assert "Reenvía tu entrega" in content
    assert "Reenviar mi entrega" in content
    # El formulario parte del envío anterior para no capturar todo otra vez.
    assert f'value="{FIRST_REPO}"' in content
    assert f'<option value="{version.pk}" selected>' in content


def test_resubmit_adds_attempt_and_returns_to_queue(
    client, student, changes_requested, lesson, new_version, environment
):
    client.force_login(student)
    response = client.post(submit_url(lesson), resubmit_data(new_version, environment))
    assert response.status_code == 302
    assert response.url == submit_url(lesson)

    changes_requested.refresh_from_db()
    assert changes_requested.status == Submission.Status.SUBMITTED
    assert Submission.objects.count() == 1
    latest = changes_requested.attempts.order_by("-submitted_at", "-pk").first()
    assert latest.repository_url == NEW_REPO
    assert latest.game_version == new_version
    assert latest.comment == "Ya agregué la instalación al README."
    assert latest.reviewer is None


@pytest.mark.parametrize(
    "status",
    [Submission.Status.SUBMITTED, Submission.Status.IN_REVIEW, Submission.Status.APPROVED],
)
def test_cannot_resubmit_unless_changes_were_requested(
    client, student, enrollment, exercise, lesson, version, environment, status
):
    make_submission(enrollment, exercise, version, environment, status=status)
    client.force_login(student)
    assert "Reenviar mi entrega" not in client.get(submit_url(lesson)).content.decode()
    client.post(submit_url(lesson), resubmit_data(version, environment))
    assert SubmissionAttempt.objects.count() == 1
    assert Submission.objects.get().status == status


def test_second_resubmit_post_does_not_add_another_attempt(
    client, student, changes_requested, lesson, version, environment
):
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(version, environment))
    client.post(submit_url(lesson), resubmit_data(version, environment, comment="Otra vez"))
    assert changes_requested.attempts.count() == 2


def test_invalid_resubmit_shows_errors_and_saves_nothing(
    client, student, changes_requested, lesson, version, environment
):
    client.force_login(student)
    response = client.post(
        submit_url(lesson), resubmit_data(version, environment, repository_url="")
    )
    assert response.status_code == 200
    assert "No se pudo enviar." in response.content.decode()
    assert changes_requested.attempts.count() == 1
    changes_requested.refresh_from_db()
    assert changes_requested.status == Submission.Status.CHANGES_REQUESTED


# Permisos: quién no puede reenviar


def test_student_with_expired_access_cannot_resubmit(
    client, student, course, exercise, lesson, version, environment, tutor, criterion
):
    submission = make_submission(
        enroll(student, course, days_left=-1), exercise, version, environment
    )
    request_changes(submission, tutor, criterion)
    client.force_login(student)
    content = client.get(submit_url(lesson)).content.decode()
    assert "Estado: Requiere cambios" in content
    assert "Reenviar mi entrega" not in content
    client.post(submit_url(lesson), resubmit_data(version, environment))
    assert submission.attempts.count() == 1


def test_anonymous_cannot_resubmit(client, changes_requested, lesson, version, environment):
    response = client.post(submit_url(lesson), resubmit_data(version, environment))
    assert response.status_code == 302
    assert reverse("accounts:login") in response.url
    assert changes_requested.attempts.count() == 1


@pytest.mark.parametrize("tutor_user", [False, True], ids=["otro-alumno", "tutor"])
def test_other_user_cannot_resubmit(
    client, changes_requested, lesson, version, environment, tutor_user
):
    client.force_login(make_user("otro@example.com", tutor=tutor_user))
    assert client.post(submit_url(lesson), resubmit_data(version, environment)).status_code == 403
    assert changes_requested.attempts.count() == 1


# Se conserva el historial de envíos y revisiones de la misma entrega


def test_resubmit_keeps_previous_attempt_and_review(
    client, student, changes_requested, lesson, new_version, environment
):
    first = changes_requested.attempts.get()
    review = first.review
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(new_version, environment))

    first.refresh_from_db()
    assert first.repository_url == FIRST_REPO
    assert first.submission == changes_requested
    review.refresh_from_db()
    assert review.attempt == first
    assert review.comment == FIRST_COMMENT
    assert review.scores.get().level == ReviewScore.Level.PARTIAL


def test_student_sees_history_of_attempts_and_reviews(
    client, student, changes_requested, lesson, new_version, environment
):
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(new_version, environment))
    content = client.get(submit_url(lesson)).content.decode()
    assert "Estado: Enviada" in content
    assert NEW_REPO in content
    assert "Envíos anteriores" in content
    assert "Envío 1 ·" in content
    assert FIRST_REPO in content
    assert FIRST_COMMENT in content
    assert "Uso de Git" in content
    # El envío nuevo todavía no tiene revisión ni se puede volver a reenviar.
    assert "La revisión de tu tutor" not in content
    assert "Reenviar mi entrega" not in content


def test_first_submission_has_no_history(
    client, student, enrollment, exercise, lesson, version, environment
):
    make_submission(enrollment, exercise, version, environment)
    client.force_login(student)
    assert "Envíos anteriores" not in client.get(submit_url(lesson)).content.decode()


def test_history_shows_every_round(
    client, student, tutor, changes_requested, lesson, version, environment, criterion
):
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(version, environment))
    request_changes(changes_requested, tutor, criterion, comment="Ahora falta la licencia.")
    client.post(
        submit_url(lesson),
        resubmit_data(version, environment, repository_url="https://github.com/ana/mi-mod-v3"),
    )
    content = client.get(submit_url(lesson)).content.decode()
    assert changes_requested.attempts.count() == 3
    assert "Envío 2 ·" in content
    assert "Envío 1 ·" in content
    assert "Ahora falta la licencia." in content
    assert FIRST_COMMENT in content


def test_other_student_does_not_see_the_history(
    client, changes_requested, course, lesson, new_version, environment, student
):
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(new_version, environment))
    other = make_user("otro@example.com")
    enroll(other, course)
    client.force_login(other)
    content = client.get(submit_url(lesson)).content.decode()
    assert FIRST_COMMENT not in content
    assert NEW_REPO not in content


def test_tutor_sees_history_on_review_page(
    client, student, tutor, changes_requested, lesson, new_version, environment
):
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(new_version, environment))
    client.force_login(tutor)
    content = client.get(reverse("reviews:review", args=[changes_requested.pk])).content.decode()
    assert NEW_REPO in content
    assert "Tomar la revisión" in content
    assert "Envíos anteriores" in content
    assert FIRST_COMMENT in content
    assert "Primer intento." in content


# El reenvío vuelve a entrar a la cola con su propia hora de envío


def test_resubmit_enters_queue_with_its_own_time(
    client, student, tutor, changes_requested, course, exercise, lesson, version, environment
):
    # Otra entrega llegó hace 2 horas; la primera de Ana, hace 30.
    other = make_submission(
        enroll(make_user("beto@example.com"), course), exercise, version, environment, hours_ago=2
    )
    client.force_login(student)
    before = timezone.now()
    client.post(submit_url(lesson), resubmit_data(version, environment))
    latest = changes_requested.attempts.order_by("-submitted_at", "-pk").first()
    assert latest.submitted_at >= before

    client.force_login(tutor)
    response = client.get(reverse("reviews:queue"))
    queued = [submission.pk for submission in response.context["submissions"]]
    # Ordena por la hora del reenvío, no por la del primer envío: va después de la otra.
    assert queued == [other.pk, changes_requested.pk]
    resubmitted = response.context["submissions"][1]
    assert resubmitted.last_submitted_at == latest.submitted_at
    assert resubmitted.attempt == latest
    assert not resubmitted.overdue


def test_tutor_reviews_the_resubmission(
    client, student, tutor, changes_requested, lesson, version, environment, criterion
):
    first = changes_requested.attempts.get()
    client.force_login(student)
    client.post(submit_url(lesson), resubmit_data(version, environment))
    latest = changes_requested.attempts.order_by("-submitted_at", "-pk").first()

    client.force_login(tutor)
    client.post(reverse("reviews:start_review", args=[changes_requested.pk]))
    latest.refresh_from_db()
    assert latest.reviewer == tutor
    client.post(
        reverse("reviews:review", args=[changes_requested.pk]),
        {
            "decision": "approved",
            "comment": "Muy bien, ya se entiende cómo instalarlo.",
            f"criterion_{criterion.pk}": "meets",
        },
    )
    changes_requested.refresh_from_db()
    assert changes_requested.status == Submission.Status.APPROVED
    assert Review.objects.get(attempt=latest).decision == Review.Decision.APPROVED
    assert Review.objects.get(attempt=first).comment == FIRST_COMMENT

    client.force_login(student)
    content = client.get(submit_url(lesson)).content.decode()
    assert "Estado: Aprobada" in content
    assert "Muy bien, ya se entiende cómo instalarlo." in content
    assert FIRST_COMMENT in content
