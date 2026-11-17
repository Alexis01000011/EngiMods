"""Métricas del piloto (EM-091)."""

import csv
import io
from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Exercise, Lesson, Module
from enrollments.models import Enrollment, LessonProgress
from metrics.views import account_metrics, course_metrics
from payments.models import Payment
from submissions.models import Review, Submission, SubmissionAttempt

pytestmark = pytest.mark.django_db

URLS = [reverse("metrics:pilot"), reverse("metrics:pilot_csv")]


def make_user(email, **kwargs):
    return get_user_model().objects.create_user(email=email, password="x-12345678", **kwargs)


def make_course(game, slug, kind, status=Course.Status.PUBLISHED):
    return Course.objects.create(
        title=slug.replace("-", " ").title(),
        slug=slug,
        game=game,
        kind=kind,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=1,
        price_cents=19900,
        access_days=30,
        status=status,
    )


def enroll(user, course, origin=Enrollment.Origin.TRIAL, status=Enrollment.Status.ACTIVE):
    return Enrollment.objects.create(user=user, course=course, origin=origin, status=status)


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
def staff():
    return make_user("admin@example.com", display_name="Admin", is_staff=True)


@pytest.fixture
def pilot(game):
    """Misión Cero con tres lecciones publicadas, una en borrador y un curso por grupos.

    - Ana pagó Misión Cero, la terminó y también está en el curso por grupos.
    - Beto entró con beca y completó una de tres lecciones (y una en borrador, que no cuenta).
    - Carla pagó, pero su inscripción está cancelada: no cuenta.
    - Dani abrió el pago y no pagó.
    - Dos revisiones en Misión Cero: de 5 y 3 horas.
    """
    practice = make_course(game, "mision-cero", Course.Kind.SHORT_PRACTICE)
    group = make_course(game, "curso-grupos", Course.Kind.COURSE)
    module = Module.objects.create(course=practice, title="Semana 1", order=1)
    lessons = [
        Lesson.objects.create(
            module=module,
            title=f"Lección {n}",
            content="Cuerpo",
            estimated_minutes=10,
            order=n,
            status=Lesson.Status.PUBLISHED,
        )
        for n in (1, 2, 3)
    ]
    draft = Lesson.objects.create(
        module=module,
        title="Borrador",
        content="Cuerpo",
        estimated_minutes=10,
        order=4,
        status=Lesson.Status.DRAFT,
    )

    ana = make_user("ana@example.com", display_name="Ana", email_verified_at=timezone.now())
    beto = make_user("beto@example.com", display_name="Beto")
    carla = make_user("carla@example.com", display_name="Carla")
    dani = make_user("dani@example.com", display_name="Dani")
    make_user("tutor@example.com", display_name="Tutor", is_tutor=True)

    ana_enrollment = enroll(ana, practice, Enrollment.Origin.STRIPE)
    enroll(ana, group)
    beto_enrollment = enroll(beto, practice, Enrollment.Origin.SCHOLARSHIP)
    enroll(carla, practice, Enrollment.Origin.STRIPE, Enrollment.Status.CANCELLED)

    for lesson in lessons:
        LessonProgress.objects.create(enrollment=ana_enrollment, lesson=lesson)
    LessonProgress.objects.create(enrollment=beto_enrollment, lesson=lessons[0])
    LessonProgress.objects.create(enrollment=beto_enrollment, lesson=draft)

    for user, status, session in [
        (ana, Payment.Status.PAID, "cs_ana"),
        (carla, Payment.Status.PAID, "cs_carla"),
        (dani, Payment.Status.PENDING, "cs_dani"),
        (dani, Payment.Status.PENDING, "cs_dani_2"),
    ]:
        Payment.objects.create(
            user=user,
            course=practice,
            amount_cents=19900,
            status=status,
            stripe_checkout_session_id=session,
        )

    exercise = Exercise.objects.create(lesson=lessons[0], title="Ejercicio", instructions="Haz.")
    version = GameVersion.objects.create(game=game, number="1.2", release_date=date(2026, 10, 1))
    environment = ModdingEnvironment.objects.create(game=game, name="Loader", version="0.9")
    reviewer = get_user_model().objects.get(email="tutor@example.com")
    sent = timezone.now() - timedelta(days=1)
    for enrollment, hours in [(ana_enrollment, 5), (beto_enrollment, 3)]:
        submission = Submission.objects.create(exercise=exercise, enrollment=enrollment)
        attempt = SubmissionAttempt.objects.create(
            submission=submission,
            repository_url="https://github.com/alumno/mod",
            game_version=version,
            modding_environment=environment,
            submitted_at=sent,
        )
        Review.objects.create(
            attempt=attempt,
            reviewer=reviewer,
            decision=Review.Decision.APPROVED,
            comment="Bien.",
            reviewed_at=sent + timedelta(hours=hours),
        )
    return practice, group


def rows_by_slug():
    return {row["course"].slug: row for row in course_metrics()}


@pytest.mark.parametrize("url", URLS)
def test_anonimo_no_ve_las_metricas(client, url):
    response = client.get(url)
    assert response.status_code == 302
    assert reverse("admin:login") in response.url


@pytest.mark.parametrize("url", URLS)
@pytest.mark.parametrize("kind", ["alumno", "tutor"])
def test_alumno_y_tutor_sin_staff_no_ven_las_metricas(client, url, kind):
    user = make_user(f"{kind}@example.com", display_name=kind, is_tutor=kind == "tutor")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 302
    assert reverse("admin:login") in response.url


def test_metricas_de_la_practica_corta(pilot):
    row = rows_by_slug()["mision-cero"]
    assert row["checkout_started"] == 3  # Ana, Carla y Dani; Dani una sola vez.
    assert row["enrollments"] == 2  # La cancelada de Carla no cuenta.
    assert row["paid"] == 1
    assert row["conversion"] == 50.0  # Ana sí está en un curso por grupos; Beto no.
    assert row["average_progress"] == 66.7  # (3/3 + 1/3) / 2; el borrador no cuenta.
    assert row["completion"] == 50.0
    assert row["reviews"] == 2
    assert row["review_hours"] == 4.0


def test_curso_por_grupos_no_tiene_conversion_ni_avance_sin_lecciones(pilot):
    row = rows_by_slug()["curso-grupos"]
    assert row["enrollments"] == 1
    assert row["conversion"] is None
    assert row["average_progress"] is None
    assert row["completion"] is None
    assert row["review_hours"] is None


def test_curso_sin_inscripciones(game):
    make_course(game, "vacio", Course.Kind.SHORT_PRACTICE, status=Course.Status.DRAFT)
    row = rows_by_slug()["vacio"]
    assert row["enrollments"] == 0
    assert row["conversion"] is None
    assert row["published"] is False


def test_cuentas_sin_contar_al_equipo(pilot, staff):
    assert account_metrics() == {"registered": 4, "verified": 1}


def test_vista_para_administradores_explica_cada_numero(client, staff, pilot):
    client.force_login(staff)
    response = client.get(reverse("metrics:pilot"))
    assert response.status_code == 200
    content = response.content.decode()
    for anchor in [
        "def-cuentas",
        "def-verificadas",
        "def-pago",
        "def-inscripciones",
        "def-pagadas",
        "def-conversion",
        "def-avance",
        "def-finalizacion",
        "def-revision",
    ]:
        assert f'href="#{anchor}"' in content
        assert f'id="{anchor}"' in content
    assert "66.7 %" in content
    assert "4 h (2 revisiones)" in content
    assert "—" in content
    assert reverse("metrics:pilot_csv") in content


def test_las_metricas_no_muestran_datos_de_personas(client, staff, pilot):
    client.force_login(staff)
    for url in URLS:
        content = client.get(url).content.decode("utf-8-sig")
        for person in ["ana@example.com", "Beto", "carla@example.com", "Dani"]:
            assert person not in content


def test_exportar_csv(client, staff, pilot):
    client.force_login(staff)
    response = client.get(reverse("metrics:pilot_csv"))
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv; charset=utf-8"
    assert response["Content-Disposition"].startswith('attachment; filename="metricas-piloto-')
    rows = list(csv.reader(io.StringIO(response.content.decode("utf-8-sig"))))
    assert rows[0][1] == "Curso"
    practice = next(row for row in rows if row[:2] == ["Juego de prueba", "Mision Cero"])
    assert practice[2:] == [
        "Práctica corta",
        "Publicado",
        "3",
        "2",
        "1",
        "50.0",
        "66.7",
        "50.0",
        "2",
        "4.0",
    ]
    group = next(row for row in rows if row[:2] == ["Juego de prueba", "Curso Grupos"])
    assert group[7:10] == ["", "", ""]
    assert ["Cuentas de alumnos registradas", "4"] in rows
    assert ["Cuentas con correo verificado", "1"] in rows


def test_primero_las_practicas_cortas(pilot):
    assert [row["course"].slug for row in course_metrics()] == ["mision-cero", "curso-grupos"]


def test_enlace_a_metricas_solo_para_el_personal(client, staff):
    student = make_user("alumno@example.com", display_name="Alumno")
    client.force_login(student)
    assert reverse("metrics:pilot") not in client.get(reverse("catalog:game_list")).content.decode()
    client.force_login(staff)
    assert reverse("metrics:pilot") in client.get(reverse("catalog:game_list")).content.decode()
