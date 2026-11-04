from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game
from courses.models import Course
from enrollments.models import Enrollment

pytestmark = pytest.mark.django_db

URL = "/mi-panel/"


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


def make_course(game, slug, status=Course.Status.PUBLISHED):
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


@pytest.fixture
def user():
    return get_user_model().objects.create_user(email="ana@example.com", password="x-12345678")


@pytest.fixture
def other():
    return get_user_model().objects.create_user(email="beto@example.com", password="x-12345678")


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


def test_url_reverse():
    assert reverse("enrollments:my_courses") == URL


def test_anonymous_is_redirected(client, user, game):
    enroll(user, make_course(game, "uno"))
    response = client.get(URL)
    assert response.status_code == 302
    assert "Curso uno" not in response.content.decode()


def test_lists_active_course_with_end_date_and_link(client, user, game):
    enrollment = enroll(user, make_course(game, "uno"), days_left=10)
    client.force_login(user)
    response = client.get(URL)
    html = response.content.decode()
    assert response.status_code == 200
    assert response.context["active"] == [enrollment]
    assert reverse("courses:course_detail", args=["uno"]) in html
    assert "Acceso hasta el" in html
    assert "Vencido" not in html


def test_expired_course_is_listed_apart_and_marked(client, user, game):
    enroll(user, make_course(game, "viejo"), days_left=-1)
    client.force_login(user)
    response = client.get(URL)
    assert response.context["active"] == []
    assert len(response.context["expired"]) == 1
    assert "Vencido" in response.content.decode()


def test_cancelled_enrollments_do_not_appear(client, user, game):
    enroll(user, make_course(game, "uno"), status=Enrollment.Status.CANCELLED)
    enroll(user, make_course(game, "dos"), days_left=-1, status=Enrollment.Status.CANCELLED)
    client.force_login(user)
    response = client.get(URL)
    assert response.context["active"] == []
    assert response.context["expired"] == []
    # Sin cursos propios, se muestra el catálogo.
    assert len(response.context["catalog"]) == 2


def test_expired_and_active_of_same_course_only_in_active(client, user, game):
    course = make_course(game, "uno")
    enroll(user, course, days_left=-5)
    enroll(user, course, days_left=10)
    client.force_login(user)
    response = client.get(URL)
    assert len(response.context["active"]) == 1
    assert response.context["expired"] == []


def test_user_only_sees_own_enrollments(client, user, other, game):
    enroll(other, make_course(game, "ajeno"), days_left=10)
    enroll(other, make_course(game, "ajeno-viejo"), days_left=-1)
    mine = enroll(user, make_course(game, "mio"))
    client.force_login(user)
    response = client.get(URL)
    assert response.context["active"] == [mine]
    assert response.context["expired"] == []
    assert "Curso ajeno" not in response.content.decode()


def test_without_courses_shows_published_catalog(client, user, game):
    make_course(game, "publicado")
    make_course(game, "borrador", status=Course.Status.DRAFT)
    client.force_login(user)
    response = client.get(URL)
    html = response.content.decode()
    assert reverse("courses:course_detail", args=["publicado"]) in html
    assert "Curso borrador" not in html
    assert "Todavía no tienes cursos" in html


def test_with_courses_does_not_show_catalog(client, user, game):
    make_course(game, "otro")
    enroll(user, make_course(game, "mio"))
    client.force_login(user)
    html = client.get(URL).content.decode()
    assert "Todavía no tienes cursos" not in html
    assert "Curso otro" not in html
