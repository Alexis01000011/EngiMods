from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonTest, Module
from enrollments.models import Enrollment, LessonProgress

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


def make_lesson(module, title, order, status=Lesson.Status.PUBLISHED, content="Cuerpo"):
    return Lesson.objects.create(
        module=module,
        title=title,
        content=content,
        estimated_minutes=10,
        order=order,
        status=status,
    )


@pytest.fixture
def course(game):
    return make_course(game)


@pytest.fixture
def module(course):
    return Module.objects.create(course=course, title="Semana 1", order=1)


@pytest.fixture
def lesson(module):
    return make_lesson(module, "Lección uno", 1, content="## Paso 1\n\n<script>alert(1)</script>")


def url(lesson, course=None):
    course = course or lesson.module.course
    return reverse("courses:lesson_detail", args=[course.slug, lesson.pk])


def make_user(email):
    return get_user_model().objects.create_user(email=email, password="x-12345678")


@pytest.fixture
def student(client, course):
    user = make_user("alumno@example.com")
    Enrollment.objects.create(user=user, course=course, origin=Enrollment.Origin.SCHOLARSHIP)
    client.force_login(user)
    return user


def test_url_is_in_spanish(lesson):
    assert url(lesson) == f"/cursos/curso-a/lecciones/{lesson.pk}/"


def test_anonymous_is_redirected_to_login(client, lesson):
    response = client.get(url(lesson))
    assert response.status_code == 302
    assert response.url.startswith(reverse("accounts:login"))
    assert "next=" in response.url


def test_enrolled_student_sees_lesson(client, lesson, student):
    response = client.get(url(lesson))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Lección uno" in html
    assert "<h2>Paso 1</h2>" in html


def test_content_is_sanitized(client, lesson, student):
    assert "<script" not in client.get(url(lesson)).content.decode()


def test_user_without_enrollment_gets_403(client, lesson):
    client.force_login(make_user("otro@example.com"))
    assert client.get(url(lesson)).status_code == 403


def test_expired_enrollment_gets_403(client, lesson, student):
    Enrollment.objects.update(access_ends_at=timezone.now() - timedelta(days=1))
    assert client.get(url(lesson)).status_code == 403


def test_cancelled_enrollment_gets_403(client, lesson, student):
    Enrollment.objects.update(status=Enrollment.Status.CANCELLED)
    assert client.get(url(lesson)).status_code == 403


def test_enrollment_in_other_course_gets_403(client, game, lesson):
    user = make_user("otro@example.com")
    Enrollment.objects.create(
        user=user, course=make_course(game, "curso-b"), origin=Enrollment.Origin.SCHOLARSHIP
    )
    client.force_login(user)
    assert client.get(url(lesson)).status_code == 403


def test_tutor_sees_lesson_without_enrollment(client, lesson):
    tutor = make_user("tutor@example.com")
    tutor.is_tutor = True
    tutor.save()
    client.force_login(tutor)
    assert client.get(url(lesson)).status_code == 200


def test_superuser_sees_lesson_without_enrollment(client, lesson):
    admin = get_user_model().objects.create_superuser(
        email="admin@example.com", password="x-12345678"
    )
    client.force_login(admin)
    assert client.get(url(lesson)).status_code == 200


def test_draft_lesson_is_404_even_for_enrolled_student(client, module, student):
    draft = make_lesson(module, "Borrador", 2, Lesson.Status.DRAFT)
    assert client.get(url(draft)).status_code == 404


def test_lesson_of_draft_course_is_404_even_for_enrolled_student(client, course, lesson, student):
    course.status = Course.Status.DRAFT
    course.save()
    assert client.get(url(lesson)).status_code == 404


def test_lesson_must_belong_to_course_in_url(client, game, lesson, student):
    other = make_course(game, "curso-b")
    assert client.get(url(lesson, other)).status_code == 404


def test_unknown_lesson_is_404(client, course, student):
    assert client.get(f"/cursos/{course.slug}/lecciones/9999/").status_code == 404


def record_test(lesson, game, number, env_version, tested_on):
    version, _ = GameVersion.objects.get_or_create(
        game=game, number=number, defaults={"release_date": date(2026, 1, 1)}
    )
    environment, _ = ModdingEnvironment.objects.get_or_create(
        game=game, name="Loader X", version=env_version
    )
    LessonTest.objects.create(
        lesson=lesson, game_version=version, modding_environment=environment, tested_on=tested_on
    )


def test_shows_tested_with_label(client, game, lesson, student):
    record_test(lesson, game, "1.2.0", "3.4", date(2026, 11, 1))
    html = client.get(url(lesson)).content.decode()
    assert "Probado con Juego de prueba 1.2.0 + Loader X 3.4" in html


def test_shows_most_recent_test(client, game, lesson, student):
    record_test(lesson, game, "1.0.0", "1.0", date(2026, 9, 1))
    record_test(lesson, game, "1.1.0", "2.0", date(2026, 10, 1))
    html = client.get(url(lesson)).content.decode()
    assert "Juego de prueba 1.1.0 + Loader X 2.0" in html
    assert "1.0.0" not in html


def test_warns_when_no_test_recorded(client, lesson, student):
    html = client.get(url(lesson)).content.decode()
    assert "no tiene una versión probada registrada" in html
    assert "Probado con" not in html


def test_navigation_follows_syllabus_across_modules_and_skips_drafts(client, course, student):
    second = Module.objects.create(course=course, title="Semana 2", order=2)
    first = Module.objects.create(course=course, title="Semana 1", order=1)
    a = make_lesson(first, "Lección A", 1)
    make_lesson(first, "Borrador B", 2, Lesson.Status.DRAFT)
    c = make_lesson(second, "Lección C", 1)
    d = make_lesson(second, "Lección D", 2)

    html_a = client.get(url(a)).content.decode()
    assert "Lección anterior" not in html_a
    assert url(c) in html_a
    assert "Borrador B" not in html_a

    html_c = client.get(url(c)).content.decode()
    assert url(a) in html_c
    assert url(d) in html_c

    html_d = client.get(url(d)).content.decode()
    assert url(c) in html_d
    assert 'rel="next"' not in html_d


# Pantalla según DESIGN.md (EM-064)


def test_syllabus_marks_current_lesson_and_completed_ones(client, course, module, student):
    first = make_lesson(module, "Primera", 1)
    current = make_lesson(module, "Actual", 2)
    enrollment = Enrollment.objects.get(user=student, course=course)
    LessonProgress.objects.create(enrollment=enrollment, lesson=first)
    html = client.get(url(current)).content.decode()
    # El temario se pinta dos veces (plegable en teléfono y lateral en escritorio).
    assert html.count(f'href="{url(current)}" aria-current="page"') == 2
    assert f'href="{url(first)}" aria-current' not in html
    assert "Completada" in html
    assert "Lección 2 de 2" in html
    assert "1 de 2 completas" in html


def test_tested_lesson_shows_stamp(client, game, lesson, student):
    record_test(lesson, game, "1.2.0", "3.4", date(2026, 11, 1))
    html = client.get(url(lesson)).content.decode()
    assert ">Probado</span>" in html


def test_untested_lesson_has_no_stamp(client, lesson, student):
    assert ">Probado</span>" not in client.get(url(lesson)).content.decode()


def test_one_primary_button_moves_to_next_lesson_after_completing(client, course, module, student):
    current = make_lesson(module, "Actual", 1)
    following = make_lesson(module, "Siguiente", 2)
    next_link = f'rel="next" href="{url(following)}" class="button-primary'

    html = client.get(url(current)).content.decode()
    assert html.count("button-primary") == 1
    assert next_link not in html

    enrollment = Enrollment.objects.get(user=student, course=course)
    LessonProgress.objects.create(enrollment=enrollment, lesson=current)
    html = client.get(url(current)).content.decode()
    assert html.count("button-primary") == 1
    assert next_link in html


def test_tutor_sees_lesson_without_primary_button(client, lesson):
    tutor = make_user("tutor@example.com")
    tutor.is_tutor = True
    tutor.save()
    client.force_login(tutor)
    html = client.get(url(lesson)).content.decode()
    assert "Lección uno" in html
    assert "button-primary" not in html
