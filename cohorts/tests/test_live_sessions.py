"""Calendario de clínicas grupales (EM-052)."""

from datetime import date, time, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game
from cohorts.models import Cohort, LiveSession
from courses.models import Course
from enrollments.models import Enrollment

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego",
        slug="juego",
        description="Un juego.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )


@pytest.fixture
def course(game):
    return Course.objects.create(
        title="Curso por grupos",
        slug="curso-por-grupos",
        game=game,
        kind=Course.Kind.COURSE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=6,
        price_cents=19900,
        access_days=10,
        status=Course.Status.PUBLISHED,
    )


def make_user(email, tutor=False):
    user = get_user_model().objects.create_user(
        email=email, password="x-12345678", display_name=email.split("@")[0]
    )
    if tutor:
        user.is_tutor = True
        user.save(update_fields=["is_tutor"])
    return user


def make_cohort(course, name, tutor):
    cohort = Cohort.objects.create(
        course=course,
        name=name,
        start_date=date(2026, 11, 1),
        end_date=date(2026, 12, 31),
        capacity=8,
    )
    cohort.tutors.add(tutor)
    return cohort


@pytest.fixture
def tutor():
    return make_user("tutora@example.com", tutor=True)


@pytest.fixture
def cohort(course, tutor):
    return make_cohort(course, "Grupo A", tutor)


@pytest.fixture
def student_and_enrollment(cohort):
    student = make_user("alumna@example.com")
    enrollment = Enrollment.objects.create(
        user=student,
        course=cohort.course,
        cohort=cohort,
        origin=Enrollment.Origin.STRIPE,
        access_ends_at=timezone.now() + timedelta(days=30),
    )
    return student, enrollment


def session_url():
    return reverse("clinics:sessions")


def test_la_fecha_pasada_se_calcula_con_la_hora_de_mexico(cohort):
    past = LiveSession.objects.create(
        cohort=cohort,
        date=date(2026, 11, 1),
        start_time=time(18, 0),
        topic="Pasada",
        join_url="https://example.com/",
    )
    future = LiveSession.objects.create(
        cohort=cohort,
        date=timezone.localdate() + timedelta(days=5),
        start_time=time(18, 0),
        topic="Futura",
        join_url="https://example.com/",
    )

    assert past.is_past
    assert not future.is_past


def test_el_tutor_registra_una_clinica(client, tutor, cohort):
    client.force_login(tutor)

    response = client.post(
        session_url(),
        {
            "cohort": cohort.pk,
            "date": "2026-12-01",
            "start_time": "18:00",
            "topic": "Revisamos los mods",
            "join_url": "https://meet.example.com/clinica",
        },
    )

    assert response.status_code == 302
    session = LiveSession.objects.get()
    assert session.cohort == cohort
    assert session.topic == "Revisamos los mods"
    assert session.start_time == time(18, 0)


def test_el_tutor_solo_ve_sus_grupos(client, tutor, cohort, course):
    other_tutor = make_user("tutorb@example.com", tutor=True)
    other_cohort = make_cohort(course, "Grupo B", other_tutor)
    client.force_login(tutor)

    html = client.get(session_url()).content.decode()

    assert "Grupo A" in html
    assert "Grupo B" not in html
    assert other_cohort not in tutor.cohorts.all()


def test_no_registra_una_clinica_en_un_grupo_ajeno(client, tutor, course):
    other_tutor = make_user("tutorb@example.com", tutor=True)
    other_cohort = make_cohort(course, "Grupo B", other_tutor)
    client.force_login(tutor)

    response = client.post(
        session_url(),
        {
            "cohort": other_cohort.pk,
            "date": "2026-12-01",
            "start_time": "18:00",
            "topic": "No debería",
            "join_url": "https://meet.example.com/clinica",
        },
    )

    assert response.status_code == 200
    assert not LiveSession.objects.exists()


def test_un_alumno_no_entra_a_las_clinicas_del_tutor(client, student_and_enrollment):
    student, _enrollment = student_and_enrollment
    client.force_login(student)

    assert client.get(session_url()).status_code == 403


def test_el_panel_muestra_las_clinicas_ordenadas_y_marca_las_pasadas(
    client, student_and_enrollment, cohort
):
    student, _enrollment = student_and_enrollment
    future = LiveSession.objects.create(
        cohort=cohort,
        date=timezone.localdate() + timedelta(days=5),
        start_time=time(18, 0),
        topic="Clínica futura",
        join_url="https://meet.example.com/futura",
    )
    past = LiveSession.objects.create(
        cohort=cohort,
        date=timezone.localdate() - timedelta(days=5),
        start_time=time(17, 0),
        topic="Clínica pasada",
        join_url="https://meet.example.com/pasada",
    )
    client.force_login(student)

    html = client.get(reverse("enrollments:my_courses")).content.decode()

    assert "Clínicas en vivo" in html
    assert html.index(past.topic) < html.index(future.topic)
    assert "Pasada" in html
    assert future.join_url in html
    assert "18:00" in html


def test_sin_clinicas_el_panel_no_muestra_la_seccion(client, student_and_enrollment):
    student, _enrollment = student_and_enrollment
    client.force_login(student)

    html = client.get(reverse("enrollments:my_courses")).content.decode()

    assert "Clínicas en vivo" not in html
