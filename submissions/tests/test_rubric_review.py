from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, Module, RubricCriterion
from enrollments.models import Enrollment
from submissions.models import Review, ReviewScore, Submission, SubmissionAttempt

pytestmark = pytest.mark.django_db

COMMENT = "Buen uso de Git. Falta explicar en el README cómo se instala."


def make_user(email, tutor=False, **kwargs):
    user = get_user_model().objects.create_user(email=email, password="x-12345678", **kwargs)
    if tutor:
        user.is_tutor = True
        user.save()
    return user


def enroll(user, course):
    now = timezone.now()
    return Enrollment.objects.create(
        user=user,
        course=course,
        origin=Enrollment.Origin.TRIAL,
        enrolled_at=now - timedelta(days=1),
        access_ends_at=now + timedelta(days=10),
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
def criteria(exercise):
    # Se crean en desorden para comprobar que se muestran por su orden.
    git = RubricCriterion.objects.create(
        exercise=exercise, title="Uso de Git", description="Commits pequeños.", order=2
    )
    works = RubricCriterion.objects.create(
        exercise=exercise, title="Funciona en la versión declarada", order=1
    )
    return [works, git]


@pytest.fixture
def student():
    return make_user("alumno@example.com", display_name="Ana")


@pytest.fixture
def tutor():
    return make_user("tutor@example.com", tutor=True, display_name="Luis")


@pytest.fixture
def submission(student, course, exercise, game):
    submission = Submission.objects.create(exercise=exercise, enrollment=enroll(student, course))
    SubmissionAttempt.objects.create(
        submission=submission,
        repository_url="https://github.com/ana/mi-mod",
        game_version=GameVersion.objects.create(
            game=game, number="1.2", release_date=date(2026, 10, 1)
        ),
        modding_environment=ModdingEnvironment.objects.create(
            game=game, name="Loader", version="0.9"
        ),
        submitted_at=timezone.now() - timedelta(hours=2),
    )
    return submission


@pytest.fixture
def taken(client, tutor, submission):
    """La entrega ya tomada por el tutor, con su sesión iniciada."""
    client.force_login(tutor)
    client.post(reverse("reviews:start_review", args=[submission.pk]))
    submission.refresh_from_db()
    assert submission.status == Submission.Status.IN_REVIEW
    return submission


def review_url(submission):
    return reverse("reviews:review", args=[submission.pk])


def submit_url(submission):
    return reverse("submissions:submit", args=[submission.exercise.lesson_id])


def review_data(criteria, decision="approved", comment=COMMENT, levels=None):
    levels = levels or ["meets"] * len(criteria)
    data = {"decision": decision, "comment": comment}
    for criterion, level in zip(criteria, levels, strict=True):
        data[f"criterion_{criterion.pk}"] = level
    return data


# Cada ejercicio tiene una rúbrica con criterios


def test_rubric_criteria_are_ordered(exercise, criteria):
    titles = list(exercise.rubric_criteria.values_list("title", flat=True))
    assert titles == ["Funciona en la versión declarada", "Uso de Git"]


def test_new_exercise_has_no_criteria_written_in_code(exercise):
    assert exercise.rubric_criteria.count() == 0


def test_admin_captures_rubric_on_exercise(client, exercise):
    admin = get_user_model().objects.create_superuser(email="admin@example.com", password="x-1")
    client.force_login(admin)
    url = reverse("admin:courses_exercise_change", args=[exercise.pk])
    assert client.get(url).status_code == 200
    response = client.post(
        url,
        {
            "lesson": exercise.lesson_id,
            "title": exercise.title,
            "instructions": exercise.instructions,
            "rubric_criteria-TOTAL_FORMS": "1",
            "rubric_criteria-INITIAL_FORMS": "0",
            "rubric_criteria-MIN_NUM_FORMS": "0",
            "rubric_criteria-MAX_NUM_FORMS": "1000",
            "rubric_criteria-0-order": "1",
            "rubric_criteria-0-title": "Documentación",
            "rubric_criteria-0-description": "El README explica cómo instalarlo.",
        },
    )
    assert response.status_code == 302
    assert list(exercise.rubric_criteria.values_list("title", flat=True)) == ["Documentación"]


def test_admin_lists_reviews(client, taken, criteria):
    client.post(review_url(taken), review_data(criteria))
    admin = get_user_model().objects.create_superuser(email="admin@example.com", password="x-1")
    client.force_login(admin)
    assert client.get(reverse("admin:submissions_review_changelist")).status_code == 200


def test_score_must_be_from_the_exercise_rubric(client, taken, criteria):
    client.post(review_url(taken), review_data(criteria))
    review = Review.objects.get()
    other_lesson = Lesson.objects.create(
        module=taken.exercise.lesson.module,
        title="Otra",
        content="Cuerpo",
        estimated_minutes=10,
        order=2,
    )
    other_exercise = Exercise.objects.create(lesson=other_lesson, title="Otro", instructions="x")
    foreign = RubricCriterion.objects.create(exercise=other_exercise, title="Ajeno", order=1)
    with pytest.raises(ValidationError):
        ReviewScore(review=review, criterion=foreign, level="meets").full_clean()


# En una pantalla propia, el tutor califica cada criterio, comenta y decide


def test_review_form_shows_each_criterion_and_decision(client, taken, criteria):
    content = client.get(review_url(taken)).content.decode()
    assert content.index("Funciona en la versión declarada") < content.index("Uso de Git")
    assert "Commits pequeños." in content
    for label in ("Cumple", "Cumple en parte", "Aún no cumple", "Aprobada", "Requiere cambios"):
        assert label in content
    assert "Comentario general" in content


def test_tutor_approves_with_rubric(client, taken, criteria, tutor):
    response = client.post(
        review_url(taken), review_data(criteria, levels=["meets", "partial"]), follow=True
    )
    assert response.redirect_chain[-1][0] == reverse("reviews:queue")
    assert "Guardamos la revisión" in response.content.decode()
    taken.refresh_from_db()
    assert taken.status == Submission.Status.APPROVED
    review = Review.objects.get()
    assert review.attempt == taken.attempts.get()
    assert review.reviewer == tutor
    assert review.decision == Review.Decision.APPROVED
    assert review.comment == COMMENT
    assert {(s.criterion.title, s.level) for s in review.scores.all()} == {
        ("Funciona en la versión declarada", "meets"),
        ("Uso de Git", "partial"),
    }
    # Ya revisada, sale de la cola.
    assert "Ejercicio uno" not in response.content.decode()


def test_tutor_requests_changes(client, taken, criteria):
    client.post(
        review_url(taken),
        review_data(criteria, decision="changes_requested", levels=["not_yet", "meets"]),
    )
    taken.refresh_from_db()
    assert taken.status == Submission.Status.CHANGES_REQUESTED
    assert Review.objects.get().decision == Review.Decision.CHANGES_REQUESTED


@pytest.mark.parametrize(
    "missing",
    ["decision", "comment", "criterion"],
    ids=["sin-decision", "sin-comentario", "sin-criterio"],
)
def test_review_needs_every_criterion_comment_and_decision(client, taken, criteria, missing):
    data = review_data(criteria)
    data.pop(f"criterion_{criteria[1].pk}" if missing == "criterion" else missing)
    response = client.post(review_url(taken), data)
    assert response.status_code == 200
    assert "No se pudo guardar." in response.content.decode()
    assert not Review.objects.exists()
    taken.refresh_from_db()
    assert taken.status == Submission.Status.IN_REVIEW


def test_empty_post_says_what_to_fix(client, taken, criteria):
    content = client.post(review_url(taken)).content.decode()
    assert "No se pudo guardar." in content
    assert content.count("Elige un nivel para este criterio.") == 2
    assert "Escribe un comentario para el alumno." in content
    assert "Elige si la apruebas o si pides cambios." in content
    assert not Review.objects.exists()


def test_invalid_level_is_rejected(client, taken, criteria):
    response = client.post(review_url(taken), review_data(criteria, levels=["meets", "excelente"]))
    assert response.status_code == 200
    assert not Review.objects.exists()


def test_exercise_without_rubric_can_still_be_reviewed(client, taken):
    content = client.get(review_url(taken)).content.decode()
    assert "todavía no tiene rúbrica" in content
    client.post(review_url(taken), review_data([]))
    review = Review.objects.get()
    assert review.scores.count() == 0
    taken.refresh_from_db()
    assert taken.status == Submission.Status.APPROVED


def test_reviewed_submission_shows_review_without_form(client, taken, criteria):
    client.post(review_url(taken), review_data(criteria, levels=["meets", "not_yet"]))
    content = client.get(review_url(taken)).content.decode()
    assert "La revisión" in content
    assert COMMENT in content
    assert "Aún no cumple" in content
    assert "Enviar la revisión" not in content
    assert "button-primary" not in content


def test_review_cannot_be_sent_twice(client, taken, criteria):
    client.post(review_url(taken), review_data(criteria))
    response = client.post(review_url(taken), review_data(criteria, decision="changes_requested"))
    assert response.status_code == 403
    assert Review.objects.count() == 1
    taken.refresh_from_db()
    assert taken.status == Submission.Status.APPROVED


def test_review_must_be_taken_first(client, tutor, submission, criteria):
    client.force_login(tutor)
    content = client.get(review_url(submission)).content.decode()
    assert "Enviar la revisión" not in content
    assert client.post(review_url(submission), review_data(criteria)).status_code == 403
    assert not Review.objects.exists()


def test_other_tutor_cannot_send_the_review(client, taken, criteria):
    client.force_login(make_user("otra-tutora@example.com", tutor=True))
    content = client.get(review_url(taken)).content.decode()
    assert "Solo el tutor que tomó la revisión puede calificarla." in content
    assert "Enviar la revisión" not in content
    assert client.post(review_url(taken), review_data(criteria)).status_code == 403
    assert not Review.objects.exists()


def test_anonymous_cannot_review(client, submission, criteria):
    assert client.post(review_url(submission), review_data(criteria)).status_code == 403
    assert not Review.objects.exists()


@pytest.mark.parametrize("kwargs", [{}, {"is_staff": True}], ids=["alumno", "staff-sin-tutor"])
def test_non_tutor_cannot_review(client, taken, criteria, kwargs):
    client.logout()
    client.force_login(make_user("no-tutor@example.com", **kwargs))
    assert client.post(review_url(taken), review_data(criteria)).status_code == 403
    assert not Review.objects.exists()


def test_student_cannot_review_own_submission(client, taken, criteria, student):
    client.force_login(student)
    assert client.post(review_url(taken), review_data(criteria)).status_code == 403
    assert not Review.objects.exists()


def test_inactive_tutor_cannot_review(client, taken, criteria, tutor):
    tutor.is_active = False
    tutor.save()
    client.force_login(tutor)
    assert client.post(review_url(taken), review_data(criteria)).status_code == 403
    assert not Review.objects.exists()


# El alumno ve la revisión completa


def test_student_sees_complete_review(client, taken, criteria, student):
    client.post(review_url(taken), review_data(criteria, levels=["meets", "partial"]))
    client.force_login(student)
    content = client.get(submit_url(taken)).content.decode()
    assert "La revisión de tu tutor" in content
    assert "Revisó Luis el" in content
    assert "Decisión: Aprobada" in content
    assert COMMENT in content
    assert "Funciona en la versión declarada" in content
    assert "Commits pequeños." in content
    assert "Cumple en parte" in content


def test_student_does_not_see_tutor_email(client, taken, criteria, student, tutor):
    tutor.display_name = ""
    tutor.save()
    client.post(review_url(taken), review_data(criteria))
    client.force_login(student)
    content = client.get(submit_url(taken)).content.decode()
    assert "Revisó Tu tutor el" in content
    assert "tutor@example.com" not in content


def test_review_comment_is_escaped(client, taken, criteria, student):
    client.post(review_url(taken), review_data(criteria, comment="<script>alert(1)</script>"))
    client.force_login(student)
    content = client.get(submit_url(taken)).content.decode()
    assert "<script>alert(1)</script>" not in content
    assert "&lt;script&gt;" in content


def test_student_sees_no_review_while_in_review(client, taken, student):
    client.force_login(student)
    assert "La revisión de tu tutor" not in client.get(submit_url(taken)).content.decode()


def test_other_student_does_not_see_the_review(client, taken, criteria, course):
    client.post(review_url(taken), review_data(criteria))
    classmate = make_user("companera@example.com")
    enroll(classmate, course)
    client.force_login(classmate)
    content = client.get(submit_url(taken)).content.decode()
    assert "La revisión de tu tutor" not in content
    assert COMMENT not in content


def test_student_without_access_cannot_open_the_review(client, taken, criteria):
    client.post(review_url(taken), review_data(criteria))
    client.force_login(make_user("sin-acceso@example.com"))
    assert client.get(submit_url(taken)).status_code == 403
