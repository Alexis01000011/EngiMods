import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.urls import reverse

from catalog.models import Game
from courses.models import Course

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego-de-prueba",
        description="Un juego para probar los cursos.",
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


def course_form_data(game, **overrides):
    data = {
        "title": "Curso desde el admin",
        "slug": "curso-desde-el-admin",
        "game": game.pk,
        "kind": Course.Kind.COURSE,
        "level": Course.Level.INTERMEDIATE,
        "description": "Descripción del curso.",
        "requirements": "Programación básica.",
        "duration_weeks": 6,
        "price_cents": 50000,
        "access_days": 90,
        "status": Course.Status.PUBLISHED,
    }
    return data | overrides


def test_curso_con_todos_sus_campos_y_borrador_por_defecto(course, game):
    course.full_clean()
    assert str(course) == "Práctica de prueba"
    assert course.game == game
    assert list(game.courses.all()) == [course]
    assert course.status == Course.Status.DRAFT


@pytest.mark.parametrize("kind", Course.Kind.values)
def test_tipos_validos(course, kind):
    course.kind = kind
    course.full_clean()


@pytest.mark.parametrize("field", ["kind", "level", "status"])
def test_rechaza_valores_fuera_de_las_opciones(course, field):
    setattr(course, field, "otro")
    with pytest.raises(ValidationError) as error:
        course.full_clean()
    assert field in error.value.message_dict


def test_niveles_disponibles():
    assert Course.Level.labels == ["Principiante", "Intermedio"]


def test_slug_unico_en_toda_la_plataforma(course):
    other_game = Game.objects.create(name="Otro juego", slug="otro-juego")
    with pytest.raises(IntegrityError):
        Course.objects.create(
            title="Otro título",
            slug=course.slug,
            game=other_game,
            duration_weeks=1,
            price_cents=0,
            access_days=1,
        )


def test_precio_en_centavos_enteros(course):
    course.refresh_from_db()
    assert course.price_cents == 12345
    assert isinstance(course.price_cents, int)


@pytest.mark.parametrize("field", ["duration_weeks", "access_days"])
def test_duracion_y_dias_de_acceso_al_menos_uno(course, field):
    setattr(course, field, 0)
    with pytest.raises(ValidationError) as error:
        course.full_clean()
    assert field in error.value.message_dict


def test_precio_no_puede_ser_negativo(course):
    course.price_cents = -1
    with pytest.raises(ValidationError) as error:
        course.full_clean()
    assert "price_cents" in error.value.message_dict


def test_solo_los_publicados_son_publicos(course, game):
    published = Course.objects.create(
        title="Curso publicado",
        slug="curso-publicado",
        game=game,
        duration_weeks=6,
        price_cents=0,
        access_days=1,
        status=Course.Status.PUBLISHED,
    )
    assert list(Course.objects.published()) == [published]
    course.status = Course.Status.PUBLISHED
    course.save()
    assert set(Course.objects.published()) == {course, published}


def test_no_se_borra_un_juego_con_cursos(course, game):
    with pytest.raises(ProtectedError):
        game.delete()
    assert Course.objects.filter(pk=course.pk).exists()


def test_administrador_crea_curso_con_precio_y_dias_de_acceso(admin_client, game):
    response = admin_client.post(reverse("admin:courses_course_add"), course_form_data(game))
    assert response.status_code == 302
    created = Course.objects.get(slug="curso-desde-el-admin")
    assert created.kind == Course.Kind.COURSE
    assert created.price_cents == 50000
    assert created.access_days == 90
    assert created.status == Course.Status.PUBLISHED


def test_admin_rechaza_slug_repetido(admin_client, course, game):
    response = admin_client.post(
        reverse("admin:courses_course_add"), course_form_data(game, slug=course.slug)
    )
    assert response.status_code == 200
    assert "slug" in response.context["adminform"].form.errors
    assert Course.objects.count() == 1


def test_admin_lista_precio_en_pesos_y_filtra_por_estado(admin_client, course):
    url = reverse("admin:courses_course_changelist")
    response = admin_client.get(url)
    assert response.status_code == 200
    assert "123.45" in response.content.decode()
    response = admin_client.get(url, {"status__exact": Course.Status.PUBLISHED})
    assert course not in response.context["cl"].queryset


@pytest.mark.parametrize("user_kind", ["anonimo", "alumno", "tutor"])
def test_sin_acceso_al_admin_no_se_puede_crear_curso(client, game, user_kind):
    if user_kind != "anonimo":
        user = get_user_model().objects.create_user(
            email=f"{user_kind}@example.com",
            display_name=user_kind,
            is_tutor=user_kind == "tutor",
        )
        client.force_login(user)
    response = client.post(reverse("admin:courses_course_add"), course_form_data(game))
    assert response.status_code == 302
    assert not Course.objects.exists()
