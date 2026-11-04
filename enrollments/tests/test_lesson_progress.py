from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game
from courses.models import Course, Lesson, Module
from enrollments.models import Enrollment, LessonProgress

pytestmark = pytest.mark.django_db

PANEL = "/mi-panel/"


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
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


def make_lesson(module, title, order, status=Lesson.Status.PUBLISHED):
    return Lesson.objects.create(
        module=module,
        title=title,
        content="Cuerpo",
        estimated_minutes=10,
        order=order,
        status=status,
    )


@pytest.fixture
def course(game):
    return make_course(game)


@pytest.fixture
def lessons(course):
    # El orden de la navegación es por módulo y luego por lección, no por pk.
    week2 = Module.objects.create(course=course, title="Semana 2", order=2)
    week1 = Module.objects.create(course=course, title="Semana 1", order=1)
    return [
        make_lesson(week1, "Uno", 1),
        make_lesson(week1, "Dos", 2),
        make_lesson(week2, "Tres", 1),
        make_lesson(week2, "Cuatro", 2),
    ]


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
def student():
    return make_user("alumno@example.com")


@pytest.fixture
def enrollment(student, course):
    return enroll(student, course)


def toggle_url(lesson):
    return reverse("enrollments:toggle_lesson", args=[lesson.pk])


def lesson_url(lesson):
    return reverse("courses:lesson_detail", args=[lesson.module.course.slug, lesson.pk])


def test_toggle_url_is_in_spanish(lessons):
    assert toggle_url(lessons[0]) == f"/mi-panel/lecciones/{lessons[0].pk}/completada/"


def test_progress_is_unique_per_enrollment_and_lesson(enrollment, lessons):
    LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])
    with pytest.raises(IntegrityError):
        LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])


def test_str(enrollment, lessons):
    progress = LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])
    assert str(progress) == f"{enrollment} · Uno"


# Botón para marcar y desmarcar


def test_lesson_shows_mark_button(client, enrollment, student, lessons):
    client.force_login(student)
    content = client.get(lesson_url(lessons[0])).content.decode()
    assert toggle_url(lessons[0]) in content
    assert "Marcar como completada" in content
    assert "Desmarcar como completada" not in content


def test_mark_then_unmark(client, enrollment, student, lessons):
    client.force_login(student)

    response = client.post(toggle_url(lessons[0]))
    assert response.status_code == 302
    assert response.url == lesson_url(lessons[0])
    assert LessonProgress.objects.filter(enrollment=enrollment, lesson=lessons[0]).exists()
    content = client.get(lesson_url(lessons[0])).content.decode()
    assert "Desmarcar como completada" in content

    client.post(toggle_url(lessons[0]))
    assert not LessonProgress.objects.exists()
    content = client.get(lesson_url(lessons[0])).content.decode()
    assert "Marcar como completada" in content


def test_get_is_not_allowed(client, enrollment, student, lessons):
    client.force_login(student)
    assert client.get(toggle_url(lessons[0])).status_code == 405
    assert not LessonProgress.objects.exists()


def test_anonymous_is_redirected(client, enrollment, lessons):
    response = client.post(toggle_url(lessons[0]))
    assert response.status_code == 302
    assert not LessonProgress.objects.exists()


def test_user_without_enrollment_is_forbidden(client, lessons):
    client.force_login(make_user("otro@example.com"))
    assert client.post(toggle_url(lessons[0])).status_code == 403
    assert not LessonProgress.objects.exists()


@pytest.mark.parametrize(
    "kwargs",
    [{"days_left": -1}, {"status": Enrollment.Status.CANCELLED}],
    ids=["vencida", "cancelada"],
)
def test_enrollment_without_access_is_forbidden(client, student, course, lessons, kwargs):
    enroll(student, course, **kwargs)
    client.force_login(student)
    assert client.post(toggle_url(lessons[0])).status_code == 403
    assert not LessonProgress.objects.exists()


def test_enrollment_in_other_course_is_forbidden(client, student, game, lessons):
    enroll(student, make_course(game, "curso-b"))
    client.force_login(student)
    assert client.post(toggle_url(lessons[0])).status_code == 403


def test_tutor_sees_lesson_without_button_and_cannot_mark(client, lessons):
    tutor = make_user("tutor@example.com")
    tutor.is_tutor = True
    tutor.save()
    client.force_login(tutor)
    response = client.get(lesson_url(lessons[0]))
    assert response.status_code == 200
    assert "Marcar como completada" not in response.content.decode()
    assert client.post(toggle_url(lessons[0])).status_code == 403


def test_draft_lesson_returns_404(client, enrollment, student, course):
    module = Module.objects.create(course=course, title="Semana 1", order=1)
    draft = make_lesson(module, "Borrador", 1, status=Lesson.Status.DRAFT)
    client.force_login(student)
    assert client.post(toggle_url(draft)).status_code == 404


def test_lesson_of_draft_course_returns_404(client, enrollment, student, course, lessons):
    course.status = Course.Status.DRAFT
    course.save()
    client.force_login(student)
    assert client.post(toggle_url(lessons[0])).status_code == 404


def test_progress_is_per_student(client, enrollment, student, course, lessons):
    other = make_user("otro@example.com")
    other_enrollment = enroll(other, course)
    LessonProgress.objects.create(enrollment=other_enrollment, lesson=lessons[0])
    client.force_login(student)
    content = client.get(lesson_url(lessons[0])).content.decode()
    assert "Desmarcar como completada" not in content


# El panel muestra el porcentaje y enlaza a la siguiente lección pendiente


def test_panel_without_progress(client, enrollment, student, lessons):
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 0 %" in content
    assert lesson_url(lessons[0]) in content


def test_panel_shows_percent_and_next_pending_lesson(client, enrollment, student, lessons):
    # Completa la primera y la tercera: falta la segunda (orden de módulo y lección).
    LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])
    LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[2])
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 50 %" in content
    assert f'href="{lesson_url(lessons[1])}"' in content
    assert "Siguiente lección: Dos" in content


def test_panel_rounds_percent_down(client, enrollment, student, course, lessons):
    module = lessons[0].module
    make_lesson(module, "Cinco", 3)
    make_lesson(module, "Seis", 4)
    LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])
    client.force_login(student)
    # 1 de 6 = 16.67 %
    assert "Avance: 16 %" in client.get(PANEL).content.decode()


def test_panel_ignores_draft_lessons(client, enrollment, student, lessons):
    draft = make_lesson(lessons[0].module, "Borrador", 0, status=Lesson.Status.DRAFT)
    LessonProgress.objects.create(enrollment=enrollment, lesson=draft)
    for lesson in lessons[:2]:
        LessonProgress.objects.create(enrollment=enrollment, lesson=lesson)
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 50 %" in content
    assert "Borrador" not in content


def test_panel_all_lessons_completed(client, enrollment, student, lessons):
    for lesson in lessons:
        LessonProgress.objects.create(enrollment=enrollment, lesson=lesson)
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 100 %" in content
    assert "Completaste todas las lecciones." in content
    assert "Siguiente lección" not in content


def test_panel_course_without_lessons(client, enrollment, student):
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 0 %" in content
    assert "Este curso aún no tiene lecciones." in content


def test_panel_shows_percent_per_course(client, enrollment, student, game, lessons):
    LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])
    other_course = make_course(game, "curso-b")
    enroll(student, other_course)
    make_lesson(Module.objects.create(course=other_course, title="M", order=1), "Única", 1)
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 25 %" in content
    assert "Avance: 0 %" in content


def test_panel_expired_course_shows_percent_without_link(client, student, course, lessons):
    expired = enroll(student, course, days_left=-1)
    LessonProgress.objects.create(enrollment=expired, lesson=lessons[0])
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Avance: 25 %" in content
    assert "Siguiente lección" not in content


def test_panel_does_not_link_lessons_of_draft_course(client, enrollment, student, course, lessons):
    course.status = Course.Status.DRAFT
    course.save()
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "Siguiente lección" not in content
    assert "Completaste todas las lecciones." not in content


def test_panel_does_not_count_progress_of_other_students(
    client, enrollment, student, course, lessons
):
    other_enrollment = enroll(make_user("otro@example.com"), course)
    LessonProgress.objects.create(enrollment=other_enrollment, lesson=lessons[0])
    client.force_login(student)
    assert "Avance: 0 %" in client.get(PANEL).content.decode()


# Pantalla según DESIGN.md (EM-064)


def test_panel_shows_completed_lessons_count_and_progress_bar(client, enrollment, student, lessons):
    LessonProgress.objects.create(enrollment=enrollment, lesson=lessons[0])
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert "1 de 4 lecciones" in content
    assert '<progress value="25" max="100"' in content


def test_panel_only_first_course_has_primary_button(client, enrollment, student, game, lessons):
    other_course = make_course(game, "curso-b")
    enroll(student, other_course)
    make_lesson(Module.objects.create(course=other_course, title="M", order=1), "Única", 1)
    client.force_login(student)
    content = client.get(PANEL).content.decode()
    assert content.count('class="button-primary') == 1
    assert content.count('class="button-secondary') == 1
