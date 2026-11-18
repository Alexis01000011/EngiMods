"""Grupos de un curso (EM-050): datos, cupo y acceso."""

from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from catalog.models import Game
from cohorts.models import Cohort
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


def make_course(game, slug="curso", kind=Course.Kind.COURSE, access_days=10):
    return Course.objects.create(
        title=f"Curso {slug}",
        slug=slug,
        game=game,
        kind=kind,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=6,
        price_cents=19900,
        access_days=access_days,
        status=Course.Status.PUBLISHED,
    )


@pytest.fixture
def course(game):
    return make_course(game)


@pytest.fixture
def cohort(course):
    return Cohort.objects.create(
        course=course,
        name="Grupo de noviembre",
        start_date=date(2026, 11, 23),
        end_date=date(2026, 12, 31),
        capacity=2,
        discord_url="https://discord.example.com/invitacion",
    )


def make_user(email):
    return get_user_model().objects.create_user(email=email, password="x-12345678")


def test_un_grupo_tiene_curso_nombre_fechas_cupo_tutores_y_estado(cohort, course):
    tutor = make_user("tutor@example.com")
    cohort.tutors.add(tutor)
    cohort.full_clean()

    assert cohort.course == course
    assert cohort.status == Cohort.Status.OPEN
    assert cohort.tutors.get() == tutor
    assert cohort.discord_url


def test_solo_los_cursos_por_grupos_tienen_grupos(game):
    practice = make_course(game, slug="practica", kind=Course.Kind.SHORT_PRACTICE)
    cohort = Cohort(
        course=practice,
        name="No debería",
        start_date=date(2026, 11, 1),
        end_date=date(2026, 11, 30),
        capacity=8,
    )

    with pytest.raises(ValidationError) as error:
        cohort.full_clean()

    assert "course" in error.value.message_dict


def test_la_fecha_de_fin_no_puede_ser_anterior_al_inicio(cohort):
    cohort.end_date = date(2026, 11, 1)

    with pytest.raises(ValidationError) as error:
        cohort.full_clean()

    assert "end_date" in error.value.message_dict


def test_el_cupo_cuenta_inscripciones_activas(cohort):
    first = make_user("uno@example.com")
    second = make_user("dos@example.com")
    Enrollment.objects.create(
        user=first, course=cohort.course, cohort=cohort, origin=Enrollment.Origin.STRIPE
    )
    Enrollment.objects.create(
        user=second, course=cohort.course, cohort=cohort, origin=Enrollment.Origin.STRIPE
    )
    assert cohort.seats_taken == 2
    assert cohort.is_full
    assert cohort.seats_left == 0


def test_no_se_inscribe_a_un_grupo_lleno(cohort):
    for index in range(2):
        Enrollment.objects.create(
            user=make_user(f"alumno{index}@example.com"),
            course=cohort.course,
            cohort=cohort,
            origin=Enrollment.Origin.STRIPE,
        )
    late = Enrollment(
        user=make_user("tarde@example.com"),
        course=cohort.course,
        cohort=cohort,
        origin=Enrollment.Origin.STRIPE,
    )

    with pytest.raises(ValidationError) as error:
        late.full_clean()

    assert "cohort" in error.value.message_dict


def test_una_inscripcion_cancelada_no_ocupa_lugar(cohort):
    Enrollment.objects.create(
        user=make_user("cancelada@example.com"),
        course=cohort.course,
        cohort=cohort,
        origin=Enrollment.Origin.STRIPE,
        status=Enrollment.Status.CANCELLED,
    )

    assert cohort.seats_taken == 0
    assert not cohort.is_full


def test_el_grupo_debe_ser_del_curso_de_la_inscripcion(cohort, game):
    other_course = make_course(game, slug="otro")
    enrollment = Enrollment(
        user=make_user("alumno@example.com"),
        course=other_course,
        cohort=cohort,
        origin=Enrollment.Origin.STRIPE,
    )

    with pytest.raises(ValidationError) as error:
        enrollment.full_clean()

    assert "cohort" in error.value.message_dict


def test_el_acceso_se_cuenta_desde_que_termina_el_grupo(cohort):
    enrollment = Enrollment(
        user=make_user("alumno@example.com"),
        course=cohort.course,
        cohort=cohort,
        origin=Enrollment.Origin.STRIPE,
        enrolled_at=timezone.now(),
    )
    enrollment.full_clean()
    enrollment.save()

    # El grupo termina el 31 de diciembre y el curso da 10 días de acceso.
    enrollment.refresh_from_db()
    assert timezone.localtime(enrollment.access_ends_at).date() == date(2027, 1, 10)
