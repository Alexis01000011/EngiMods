import pytest
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game
from core.models import LegalText
from courses.models import Course, Lesson, Module

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
        title="Práctica de prueba",
        slug="practica-de-prueba",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisito único de prueba.",
        duration_weeks=3,
        price_cents=12345,
        access_days=45,
        status=Course.Status.PUBLISHED,
    )


def make_lesson(module, title, order, status=Lesson.Status.PUBLISHED):
    return Lesson.objects.create(
        module=module,
        title=title,
        content="SECRETO del contenido",
        estimated_minutes=10,
        order=order,
        status=status,
    )


def url(course):
    return reverse("courses:course_detail", args=[course.slug])


def test_url_is_in_spanish(course):
    assert url(course) == "/cursos/practica-de-prueba/"


def test_shows_course_data(client, course):
    response = client.get(url(course))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Requisito único de prueba." in html
    assert "3 semanas" in html
    assert "45 días" in html
    assert "MXN 123.45" in html


def test_data_comes_from_course(client, course):
    course.duration_weeks = 1
    course.access_days = 1
    course.price_cents = 10000
    course.save()
    html = client.get(url(course)).content.decode()
    assert "1 semana." in html
    assert "1 día." in html
    assert "MXN 100.00" in html


def test_draft_course_is_404(client, course):
    course.status = Course.Status.DRAFT
    course.save()
    assert client.get(url(course)).status_code == 404


def test_unknown_course_is_404(client):
    assert client.get("/cursos/no-existe/").status_code == 404


def test_syllabus_orders_modules_and_hides_draft_lessons(client, course):
    second = Module.objects.create(course=course, title="Módulo dos", order=2)
    first = Module.objects.create(course=course, title="Módulo uno", order=1)
    make_lesson(first, "Lección B", 2)
    make_lesson(first, "Lección A", 1)
    make_lesson(first, "Lección borrador", 3, Lesson.Status.DRAFT)
    make_lesson(second, "Lección C", 1)
    html = client.get(url(course)).content.decode()
    assert html.index("Módulo uno") < html.index("Módulo dos")
    assert html.index("Lección A") < html.index("Lección B") < html.index("Lección C")
    assert "Lección borrador" not in html


def test_lesson_content_is_not_shown(client, course):
    make_lesson(Module.objects.create(course=course, title="M", order=1), "L", 1)
    assert "SECRETO" not in client.get(url(course)).content.decode()


def test_refund_policy_is_provisional_without_terms(client, course):
    html = client.get(url(course)).content.decode()
    assert "Política de devolución" in html
    assert "Texto provisional" in html
    assert "pendiente de publicarse" in html
    assert reverse("core:terms") not in html


def test_refund_policy_links_to_terms_when_current(client, course):
    LegalText.objects.create(
        kind=LegalText.Kind.TERMS,
        version="1.0",
        body="Texto de prueba.",
        effective_date=timezone.localdate(),
    )
    html = client.get(url(course)).content.decode()
    assert 'id="politica-de-devolucion"' in html
    assert f'href="{reverse("core:terms")}"' in html
    assert "Texto provisional" not in html


def test_anonymous_can_view(client, course):
    assert client.get(url(course)).status_code == 200


def test_links_to_active_game(client, course):
    html = client.get(url(course)).content.decode()
    assert reverse("catalog:game_detail", args=[course.game.slug]) in html


def test_hidden_game_is_not_linked(client, course):
    course.game.status = Game.Status.HIDDEN
    course.game.save()
    response = client.get(url(course))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Juego de prueba" in html
    assert reverse("catalog:game_detail", args=[course.game.slug]) not in html
