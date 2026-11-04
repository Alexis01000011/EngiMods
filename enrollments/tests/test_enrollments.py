from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game
from courses.models import Course
from enrollments.models import Enrollment

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego para probar las inscripciones.",
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
        description="Una práctica para probar el modelo.",
        requirements="Computadora y el juego.",
        duration_weeks=1,
        price_cents=12345,
        access_days=30,
    )


@pytest.fixture
def student():
    return get_user_model().objects.create_user(email="alumno@example.com", password="x-12345678")


def enroll(student, course, **kwargs):
    kwargs.setdefault("origin", Enrollment.Origin.SCHOLARSHIP)
    return Enrollment.objects.create(user=student, course=course, **kwargs)


def test_access_end_is_calculated_with_course_access_days(student, course):
    enrollment = enroll(student, course)
    assert enrollment.status == Enrollment.Status.ACTIVE
    assert enrollment.access_ends_at == enrollment.enrolled_at + timedelta(days=30)


def test_access_end_follows_the_course_access_days_at_creation(student, course):
    course.access_days = 90
    course.save()
    enrollment = enroll(student, course)
    assert enrollment.access_ends_at == enrollment.enrolled_at + timedelta(days=90)


def test_access_end_calculated_when_validating_from_a_form(student, course):
    enrollment = Enrollment(user=student, course=course, origin=Enrollment.Origin.TRIAL)
    enrollment.full_clean()
    assert enrollment.access_ends_at == enrollment.enrolled_at + timedelta(days=30)


def test_active_enrollment_before_end_has_access(student, course):
    enrollment = enroll(student, course)
    assert enrollment.has_access
    assert not enrollment.is_expired
    assert list(Enrollment.objects.with_access()) == [enrollment]


def test_expired_enrollment_has_no_access_and_is_not_stored_as_status(student, course):
    enrollment = enroll(student, course, access_ends_at=timezone.now() - timedelta(seconds=1))
    assert enrollment.status == Enrollment.Status.ACTIVE
    assert enrollment.is_expired
    assert not enrollment.has_access
    assert not Enrollment.objects.with_access().exists()
    assert "expired" not in Enrollment.Status.values


def test_cancelled_enrollment_has_no_access(student, course):
    enrollment = enroll(student, course, status=Enrollment.Status.CANCELLED)
    assert not enrollment.has_access
    assert not enrollment.is_expired
    assert not Enrollment.objects.with_access().exists()


def test_cannot_have_two_enrollments_with_access_to_the_same_course(student, course):
    enroll(student, course)
    second = Enrollment(user=student, course=course, origin=Enrollment.Origin.TRIAL)
    with pytest.raises(ValidationError):
        second.full_clean()


def test_editing_the_only_current_enrollment_is_valid(student, course):
    enrollment = enroll(student, course)
    enrollment.origin = Enrollment.Origin.EXTERNAL_PAYMENT
    enrollment.full_clean()


def test_can_enroll_again_after_access_expired(student, course):
    enroll(student, course, access_ends_at=timezone.now() - timedelta(days=1))
    again = Enrollment(user=student, course=course, origin=Enrollment.Origin.EXTERNAL_PAYMENT)
    again.full_clean()
    again.save()
    assert Enrollment.objects.with_access().get() == again


def test_can_enroll_again_after_cancellation(student, course):
    enroll(student, course, status=Enrollment.Status.CANCELLED)
    again = Enrollment(user=student, course=course, origin=Enrollment.Origin.SCHOLARSHIP)
    again.full_clean()


def test_current_enrollment_in_another_course_or_of_another_student_does_not_block(
    student, course, game
):
    other_course = Course.objects.create(
        title="Otra práctica",
        slug="otra-practica",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Otra.",
        requirements="Ninguno.",
        duration_weeks=1,
        price_cents=0,
        access_days=10,
    )
    other_student = get_user_model().objects.create_user(
        email="otra@example.com", password="x-12345678"
    )
    enroll(student, course)
    Enrollment(user=student, course=other_course, origin=Enrollment.Origin.TRIAL).full_clean()
    Enrollment(user=other_student, course=course, origin=Enrollment.Origin.TRIAL).full_clean()


def test_origin_distinguishes_stripe_from_manual(student, course):
    assert {"stripe", "scholarship", "trial", "external_payment"} == set(Enrollment.Origin.values)
    enroll(student, course, origin=Enrollment.Origin.STRIPE)
    assert Enrollment.objects.filter(origin=Enrollment.Origin.STRIPE).count() == 1
    assert not Enrollment.objects.filter(origin=Enrollment.Origin.SCHOLARSHIP).exists()


def test_user_and_course_with_enrollments_are_protected(student, course):
    enroll(student, course)
    with pytest.raises(ProtectedError):
        course.delete()
    with pytest.raises(ProtectedError):
        student.delete()


def test_str(student, course):
    assert str(enroll(student, course)) == f"{student} · {course}"


@pytest.fixture
def admin_client(client):
    admin = get_user_model().objects.create_superuser(
        email="admin@example.com", password="x-12345678"
    )
    client.force_login(admin)
    return client


def test_admin_creates_manual_enrollment_with_calculated_end(admin_client, student, course):
    response = admin_client.post(
        reverse("admin:enrollments_enrollment_add"),
        {
            "user": student.pk,
            "course": course.pk,
            "origin": Enrollment.Origin.SCHOLARSHIP,
            "status": Enrollment.Status.ACTIVE,
            "enrolled_at_0": "2026-11-10",
            "enrolled_at_1": "12:00:00",
            "access_ends_at_0": "",
            "access_ends_at_1": "",
        },
    )
    assert response.status_code == 302
    enrollment = Enrollment.objects.get()
    assert enrollment.origin == Enrollment.Origin.SCHOLARSHIP
    assert enrollment.access_ends_at == enrollment.enrolled_at + timedelta(days=30)


def test_admin_rejects_second_current_enrollment(admin_client, student, course):
    enroll(student, course)
    response = admin_client.post(
        reverse("admin:enrollments_enrollment_add"),
        {
            "user": student.pk,
            "course": course.pk,
            "origin": Enrollment.Origin.TRIAL,
            "status": Enrollment.Status.ACTIVE,
            "enrolled_at_0": timezone.localdate().isoformat(),
            "enrolled_at_1": "00:00:00",
            "access_ends_at_0": "",
            "access_ends_at_1": "",
        },
    )
    assert response.status_code == 200
    assert Enrollment.objects.count() == 1


def test_admin_list_filters_by_origin_and_status(admin_client, student, course):
    enroll(student, course, origin=Enrollment.Origin.STRIPE)
    url = reverse("admin:enrollments_enrollment_changelist")
    assert (
        admin_client.get(url, {"origin__exact": "stripe", "status__exact": "active"}).status_code
        == 200
    )
    response = admin_client.get(url, {"q": "alumno@example.com"})
    assert response.status_code == 200
    assert "alumno@example.com" in response.content.decode()


def test_admin_is_closed_to_non_staff(client, student, course):
    client.force_login(student)
    response = client.get(reverse("admin:enrollments_enrollment_changelist"))
    assert response.status_code == 302
