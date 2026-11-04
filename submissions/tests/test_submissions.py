from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, Module
from enrollments.models import Enrollment
from submissions.models import Submission, SubmissionAttempt
from submissions.validators import validate_git_repository_url

pytestmark = pytest.mark.django_db

REPO = "https://github.com/ana/mi-mod"


def make_game(slug="juego-a"):
    return Game.objects.create(
        name=f"Juego {slug}",
        slug=slug,
        description="Un juego.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


def make_course(game, slug="curso-a", status=Course.Status.PUBLISHED):
    return Course.objects.create(
        title=f"Curso {slug}",
        slug=slug,
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=1,
        price_cents=10000,
        access_days=30,
        status=status,
    )


def make_lesson(course, title="Lección uno", status=Lesson.Status.PUBLISHED):
    module, _ = Module.objects.get_or_create(course=course, title="Semana 1", order=1)
    return Lesson.objects.create(
        module=module,
        title=title,
        content="Cuerpo",
        estimated_minutes=10,
        order=module.lessons.count() + 1,
        status=status,
    )


def make_user(email):
    return get_user_model().objects.create_user(email=email, password="x-12345678")


def enroll(user, course, days_left=10, **kwargs):
    now = timezone.now()
    return Enrollment.objects.create(
        user=user,
        course=course,
        origin=Enrollment.Origin.TRIAL,
        enrolled_at=now - timedelta(days=30),
        access_ends_at=now + timedelta(days=days_left),
        **kwargs,
    )


@pytest.fixture
def game():
    return make_game()


@pytest.fixture
def version(game):
    return GameVersion.objects.create(game=game, number="1.2", release_date=date(2026, 10, 1))


@pytest.fixture
def environment(game):
    return ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9")


@pytest.fixture
def course(game):
    return make_course(game)


@pytest.fixture
def lesson(course):
    return make_lesson(course)


@pytest.fixture
def exercise(lesson):
    return Exercise.objects.create(
        lesson=lesson,
        title="Tu primer mod",
        instructions="Crea un repositorio.\n\n<script>alert(1)</script>",
    )


@pytest.fixture
def student():
    return make_user("alumno@example.com")


@pytest.fixture
def enrollment(student, course):
    return enroll(student, course)


def submit_url(lesson):
    return reverse("submissions:submit", args=[lesson.pk])


def lesson_url(lesson):
    return reverse("courses:lesson_detail", args=[lesson.module.course.slug, lesson.pk])


def form_data(version, environment, **overrides):
    data = {
        "repository_url": REPO,
        "game_version": version.pk,
        "modding_environment": environment.pk,
        "comment": "Funciona en mi computadora.",
    }
    data.update(overrides)
    return data


def make_submission(enrollment, exercise, version, environment, **kwargs):
    submission = Submission.objects.create(exercise=exercise, enrollment=enrollment, **kwargs)
    SubmissionAttempt.objects.create(
        submission=submission,
        repository_url=REPO,
        game_version=version,
        modding_environment=environment,
    )
    return submission


def test_urls_are_in_spanish(lesson):
    assert submit_url(lesson) == f"/mi-panel/entregas/lecciones/{lesson.pk}/"
    assert reverse("submissions:my_submissions") == "/mi-panel/entregas/"


# Una lección puede definir un ejercicio entregable con instrucciones


def test_lesson_can_define_exercise(exercise, lesson):
    assert lesson.exercise == exercise
    assert str(exercise) == "Tu primer mod"


def test_admin_adds_exercise_to_lesson(admin_client, lesson):
    data = {
        "module": lesson.module.pk,
        "title": lesson.title,
        "content": lesson.content,
        "estimated_minutes": 10,
        "order": lesson.order,
        "status": lesson.status,
        "tests-TOTAL_FORMS": 0,
        "tests-INITIAL_FORMS": 0,
        "tests-MIN_NUM_FORMS": 0,
        "tests-MAX_NUM_FORMS": 1000,
        "exercise-TOTAL_FORMS": 1,
        "exercise-INITIAL_FORMS": 0,
        "exercise-MIN_NUM_FORMS": 0,
        "exercise-MAX_NUM_FORMS": 1,
        "exercise-0-title": "Desde el admin",
        "exercise-0-instructions": "Sube tu mod.",
    }
    response = admin_client.post(reverse("admin:courses_lesson_change", args=[lesson.pk]), data)
    assert response.status_code == 302
    assert Exercise.objects.get(lesson=lesson).title == "Desde el admin"


def test_exercise_is_one_per_lesson(exercise, lesson):
    with pytest.raises(IntegrityError):
        Exercise.objects.create(lesson=lesson, title="Otro", instructions="x")


def test_exercise_instructions_are_sanitized(exercise):
    assert "<script>" not in exercise.instructions_html
    assert "Crea un repositorio." in exercise.instructions_html


def test_lesson_page_shows_exercise_and_link(client, enrollment, student, exercise, lesson):
    client.force_login(student)
    content = client.get(lesson_url(lesson)).content.decode()
    assert "Ejercicio: Tu primer mod" in content
    assert submit_url(lesson) in content


def test_lesson_without_exercise_has_no_link(client, enrollment, student, lesson):
    client.force_login(student)
    content = client.get(lesson_url(lesson)).content.decode()
    assert submit_url(lesson) not in content


def test_submit_page_shows_instructions_and_form(
    client, enrollment, student, exercise, lesson, version, environment
):
    client.force_login(student)
    response = client.get(submit_url(lesson))
    content = response.content.decode()
    assert response.status_code == 200
    assert "Crea un repositorio." in content
    assert "<script>alert(1)</script>" not in content
    assert "Enviar entrega" in content


def test_lesson_without_exercise_returns_404(client, enrollment, student, lesson):
    client.force_login(student)
    assert client.get(submit_url(lesson)).status_code == 404


def test_exercise_of_draft_lesson_returns_404(client, student, course):
    enroll(student, course)
    draft = make_lesson(course, "Borrador", status=Lesson.Status.DRAFT)
    Exercise.objects.create(lesson=draft, title="E", instructions="x")
    client.force_login(student)
    assert client.get(submit_url(draft)).status_code == 404


def test_exercise_of_draft_course_returns_404(client, enrollment, student, exercise, course):
    course.status = Course.Status.DRAFT
    course.save()
    client.force_login(student)
    assert client.get(submit_url(exercise.lesson)).status_code == 404


# La entrega queda ligada a la inscripción del alumno


def test_submit_creates_submission_linked_to_enrollment(
    client, enrollment, student, exercise, lesson, version, environment
):
    client.force_login(student)
    response = client.post(submit_url(lesson), form_data(version, environment))
    assert response.status_code == 302
    assert response.url == submit_url(lesson)
    submission = Submission.objects.get()
    assert submission.enrollment == enrollment
    assert submission.exercise == exercise
    assert submission.status == Submission.Status.SUBMITTED


def test_submission_uses_the_enrollment_with_access(
    client, student, course, exercise, lesson, version, environment
):
    enroll(student, course, days_left=-5)
    current = enroll(student, course)
    client.force_login(student)
    client.post(submit_url(lesson), form_data(version, environment))
    assert Submission.objects.get().enrollment == current


def test_submission_is_unique_per_exercise_and_enrollment(
    enrollment, exercise, version, environment
):
    make_submission(enrollment, exercise, version, environment)
    with pytest.raises(IntegrityError):
        Submission.objects.create(exercise=exercise, enrollment=enrollment)


def test_submission_exercise_must_be_of_enrollment_course(student, game, exercise):
    other = enroll(student, make_course(game, "curso-b"))
    submission = Submission(exercise=exercise, enrollment=other)
    with pytest.raises(ValidationError) as error:
        submission.full_clean()
    assert "exercise" in error.value.message_dict


def test_second_post_does_not_create_another_submission(
    client, enrollment, student, exercise, lesson, version, environment
):
    client.force_login(student)
    client.post(submit_url(lesson), form_data(version, environment))
    client.post(submit_url(lesson), form_data(version, environment, comment="Otra vez"))
    assert Submission.objects.count() == 1
    assert SubmissionAttempt.objects.count() == 1


def test_anonymous_is_redirected(client, exercise, lesson, version, environment):
    response = client.post(submit_url(lesson), form_data(version, environment))
    assert response.status_code == 302
    assert not Submission.objects.exists()


def test_user_without_enrollment_is_forbidden(client, exercise, lesson, version, environment):
    client.force_login(make_user("otro@example.com"))
    assert client.get(submit_url(lesson)).status_code == 403
    assert client.post(submit_url(lesson), form_data(version, environment)).status_code == 403
    assert not Submission.objects.exists()


@pytest.mark.parametrize(
    "kwargs",
    [{"days_left": -1}, {"status": Enrollment.Status.CANCELLED}],
    ids=["vencida", "cancelada"],
)
def test_enrollment_without_access_cannot_submit(
    client, student, course, exercise, lesson, version, environment, kwargs
):
    enroll(student, course, **kwargs)
    client.force_login(student)
    assert client.post(submit_url(lesson), form_data(version, environment)).status_code == 403
    assert not Submission.objects.exists()


def test_tutor_cannot_submit(client, exercise, lesson, version, environment):
    tutor = make_user("tutor@example.com")
    tutor.is_tutor = True
    tutor.save()
    client.force_login(tutor)
    assert client.post(submit_url(lesson), form_data(version, environment)).status_code == 403


# Enlace al repositorio Git (obligatorio), comentario y versión del juego y entorno


def test_attempt_stores_repository_comment_version_and_environment(
    client, enrollment, student, exercise, lesson, version, environment
):
    client.force_login(student)
    client.post(submit_url(lesson), form_data(version, environment))
    attempt = SubmissionAttempt.objects.get()
    assert attempt.repository_url == REPO
    assert attempt.comment == "Funciona en mi computadora."
    assert attempt.game_version == version
    assert attempt.modding_environment == environment
    assert attempt.submitted_at is not None


def test_comment_is_optional(client, enrollment, student, exercise, lesson, version, environment):
    client.force_login(student)
    client.post(submit_url(lesson), form_data(version, environment, comment=""))
    assert SubmissionAttempt.objects.get().comment == ""


@pytest.mark.parametrize("field", ["repository_url", "game_version", "modding_environment"])
def test_required_fields(
    client, enrollment, student, exercise, lesson, version, environment, field
):
    client.force_login(student)
    response = client.post(submit_url(lesson), form_data(version, environment, **{field: ""}))
    assert response.status_code == 200
    assert field in response.context["form"].errors
    assert not Submission.objects.exists()


def test_versions_of_other_game_are_rejected(
    client, enrollment, student, exercise, lesson, version, environment
):
    other_game = make_game("juego-b")
    other_version = GameVersion.objects.create(
        game=other_game, number="9.9", release_date=date(2026, 1, 1)
    )
    other_environment = ModdingEnvironment.objects.create(game=other_game, name="Otro", version="1")
    client.force_login(student)
    response = client.post(
        submit_url(lesson),
        form_data(
            version,
            environment,
            game_version=other_version.pk,
            modding_environment=other_environment.pk,
        ),
    )
    errors = response.context["form"].errors
    assert "game_version" in errors
    assert "modding_environment" in errors
    assert "9.9" not in response.content.decode()
    assert not Submission.objects.exists()


def test_attempt_model_rejects_versions_of_other_game(enrollment, exercise, version, environment):
    other_game = make_game("juego-b")
    submission = Submission.objects.create(exercise=exercise, enrollment=enrollment)
    attempt = SubmissionAttempt(
        submission=submission,
        repository_url=REPO,
        game_version=GameVersion.objects.create(
            game=other_game, number="9.9", release_date=date(2026, 1, 1)
        ),
        modding_environment=ModdingEnvironment.objects.create(
            game=other_game, name="Otro", version="1"
        ),
    )
    with pytest.raises(ValidationError) as error:
        attempt.full_clean()
    assert set(error.value.message_dict) >= {"game_version", "modding_environment"}


# Se valida que el enlace sea una URL de un servicio Git


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/ana/mi-mod",
        "https://www.github.com/ana/mi-mod",
        "https://gitlab.com/grupo/subgrupo/mi-mod",
        "https://bitbucket.org/ana/mi-mod",
        "https://codeberg.org/ana/mi-mod.git",
        "https://GitHub.com/Ana/Mi-Mod",
    ],
)
def test_valid_git_urls(url):
    validate_git_repository_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/ana/mi-mod",
        "https://example.com/ana/mi-mod",
        "https://github.com.evil.com/ana/mi-mod",
        "https://evilgithub.com/ana/mi-mod",
        "https://github.com/ana",
        "https://github.com/",
        "git@github.com:ana/mi-mod.git",
        "javascript:alert(1)",
    ],
)
def test_invalid_git_urls(url):
    with pytest.raises(ValidationError):
        validate_git_repository_url(url)


@override_settings(GIT_REPOSITORY_HOSTS=["git.example.org"])
def test_git_hosts_come_from_settings():
    validate_git_repository_url("https://git.example.org/ana/mi-mod")
    with pytest.raises(ValidationError):
        validate_git_repository_url("https://github.com/ana/mi-mod")


def test_form_rejects_non_git_url(
    client, enrollment, student, exercise, lesson, version, environment
):
    client.force_login(student)
    response = client.post(
        submit_url(lesson),
        form_data(version, environment, repository_url="https://example.com/ana/mi-mod"),
    )
    assert "repository_url" in response.context["form"].errors
    assert "servicio Git" in response.content.decode()
    assert not Submission.objects.exists()


# El alumno ve el estado


@pytest.mark.parametrize(
    ("status", "label"),
    [
        (Submission.Status.SUBMITTED, "Enviada"),
        (Submission.Status.IN_REVIEW, "En revisión"),
        (Submission.Status.APPROVED, "Aprobada"),
        (Submission.Status.CHANGES_REQUESTED, "Requiere cambios"),
    ],
)
def test_student_sees_status(
    client, enrollment, student, exercise, lesson, version, environment, status, label
):
    make_submission(enrollment, exercise, version, environment, status=status)
    client.force_login(student)
    assert f"Estado: {label}" in client.get(submit_url(lesson)).content.decode()
    assert label in client.get(reverse("submissions:my_submissions")).content.decode()
    assert f"Tu entrega: {label}." in client.get(lesson_url(lesson)).content.decode()


def test_submit_page_shows_submission_instead_of_form(
    client, enrollment, student, exercise, lesson, version, environment
):
    make_submission(enrollment, exercise, version, environment)
    client.force_login(student)
    content = client.get(submit_url(lesson)).content.decode()
    assert REPO in content
    assert "1.2 + Loader 0.9" in content
    assert "Enviar entrega" not in content


def test_student_with_expired_access_still_sees_own_submission(
    client, student, course, exercise, lesson, version, environment
):
    expired = enroll(student, course, days_left=-1)
    make_submission(expired, exercise, version, environment, status=Submission.Status.APPROVED)
    client.force_login(student)
    response = client.get(submit_url(lesson))
    assert response.status_code == 200
    assert "Estado: Aprobada" in response.content.decode()
    assert "Enviar entrega" not in response.content.decode()


def test_my_submissions_only_lists_own(client, student, course, exercise, version, environment):
    make_submission(enroll(student, course), exercise, version, environment)
    other = make_user("otro@example.com")
    client.force_login(other)
    content = client.get(reverse("submissions:my_submissions")).content.decode()
    assert "Tu primer mod" not in content
    assert "Todavía no has enviado ninguna entrega." in content


def test_other_student_does_not_see_submission(
    client, enrollment, course, exercise, lesson, version, environment
):
    make_submission(enrollment, exercise, version, environment)
    other = make_user("otro@example.com")
    enroll(other, course)
    client.force_login(other)
    content = client.get(submit_url(lesson)).content.decode()
    assert REPO not in content
    assert "Enviar entrega" in content


def test_my_submissions_requires_login(client):
    assert client.get(reverse("submissions:my_submissions")).status_code == 302


def test_panel_links_to_my_submissions(client, enrollment, student):
    client.force_login(student)
    content = client.get(reverse("enrollments:my_courses")).content.decode()
    assert reverse("submissions:my_submissions") in content


def test_admin_lists_submissions(admin_client, enrollment, exercise, version, environment):
    submission = make_submission(enrollment, exercise, version, environment)
    response = admin_client.get(reverse("admin:submissions_submission_changelist"))
    assert response.status_code == 200
    assert "Tu primer mod" in response.content.decode()
    detail = admin_client.get(reverse("admin:submissions_submission_change", args=[submission.pk]))
    assert REPO in detail.content.decode()
