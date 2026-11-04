from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.urls import reverse

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonTest, Module

pytestmark = pytest.mark.django_db


def make_game(slug):
    game = Game.objects.create(name=f"Juego {slug}", slug=slug, official_url="https://example.com/")
    version = GameVersion.objects.create(game=game, number="1.0", release_date=date(2026, 1, 1))
    environment = ModdingEnvironment.objects.create(game=game, name="Loader", version="0.1")
    environment.compatible_versions.add(version)
    return game, version, environment


def make_course(game, slug):
    return Course.objects.create(
        title=f"Curso {slug}",
        slug=slug,
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=1,
        price_cents=0,
        access_days=30,
    )


def make_lesson(module, order=1, **fields):
    return Lesson.objects.create(
        module=module,
        title=fields.pop("title", f"Lección {order}"),
        content=fields.pop("content", "Contenido."),
        estimated_minutes=fields.pop("estimated_minutes", 15),
        order=order,
        **fields,
    )


@pytest.fixture
def game():
    return make_game("juego-a")


@pytest.fixture
def other_game():
    return make_game("juego-b")


@pytest.fixture
def module(game):
    return Module.objects.create(course=make_course(game[0], "curso-a"), title="Semana 1", order=1)


@pytest.fixture
def lesson(module):
    return make_lesson(module)


@pytest.fixture
def tested_lesson(lesson, game):
    _, version, environment = game
    LessonTest.objects.create(
        lesson=lesson,
        game_version=version,
        modding_environment=environment,
        tested_on=date(2026, 11, 1),
    )
    return lesson


def test_modulos_y_lecciones_ordenados(module):
    course = module.course
    second_module = Module.objects.create(course=course, title="Semana 2", order=2)
    first_module = Module.objects.create(course=course, title="Semana 0", order=0)
    assert list(course.modules.all()) == [first_module, module, second_module]
    third = make_lesson(module, order=3)
    first = make_lesson(module, order=1)
    second = make_lesson(module, order=2)
    assert list(module.lessons.all()) == [first, second, third]


def test_leccion_con_todos_sus_campos_y_borrador_por_defecto(lesson):
    lesson.full_clean()
    assert str(lesson) == "Lección 1"
    assert lesson.status == Lesson.Status.DRAFT
    assert lesson.estimated_minutes == 15


def test_duracion_estimada_de_al_menos_un_minuto(lesson):
    lesson.estimated_minutes = 0
    with pytest.raises(ValidationError) as error:
        lesson.full_clean()
    assert "estimated_minutes" in error.value.message_dict


def test_rechaza_estado_fuera_de_las_opciones(lesson):
    lesson.status = "otro"
    with pytest.raises(ValidationError) as error:
        lesson.full_clean()
    assert "status" in error.value.message_dict


def test_las_lecciones_en_borrador_no_son_para_alumnos(lesson, module):
    published = make_lesson(module, order=2, status=Lesson.Status.PUBLISHED)
    assert list(Lesson.objects.published()) == [published]
    assert list(module.lessons.published()) == [published]


def test_contenido_markdown_se_muestra_como_html_seguro(module):
    lesson = make_lesson(module, content="## Paso 1\n\n<script>alert(1)</script>")
    assert "<h2>Paso 1</h2>" in lesson.content_html
    assert "<script" not in lesson.content_html


def test_registra_probado_con_version_entorno_y_fecha(tested_lesson, game):
    _, version, environment = game
    test = tested_lesson.tests.get()
    test.full_clean()
    assert test.game_version == version
    assert test.modding_environment == environment
    assert test.tested_on == date(2026, 11, 1)
    assert str(test) == "Juego juego-a 1.0 · Loader 0.1 (2026-11-01)"


def test_la_prueba_mas_reciente_va_primero(tested_lesson, game):
    _, version, environment = game
    newest = LessonTest.objects.create(
        lesson=tested_lesson,
        game_version=version,
        modding_environment=environment,
        tested_on=date(2026, 11, 3),
    )
    assert tested_lesson.tests.first() == newest


@pytest.mark.parametrize("field", ["game_version", "modding_environment"])
def test_probado_con_debe_ser_del_juego_del_curso(lesson, game, other_game, field):
    _, version, environment = game
    _, other_version, other_environment = other_game
    test = LessonTest(
        lesson=lesson,
        game_version=other_version if field == "game_version" else version,
        modding_environment=other_environment if field == "modding_environment" else environment,
        tested_on=date(2026, 11, 1),
    )
    with pytest.raises(ValidationError) as error:
        test.full_clean()
    assert list(error.value.message_dict) == [field]


def test_no_se_cambia_el_juego_de_un_curso_con_lecciones_probadas(tested_lesson, other_game):
    course = tested_lesson.module.course
    course.game = other_game[0]
    with pytest.raises(ValidationError) as error:
        course.full_clean()
    assert "game" in error.value.message_dict


def test_no_se_mueve_un_modulo_probado_a_un_curso_de_otro_juego(tested_lesson, other_game):
    module = tested_lesson.module
    module.course = make_course(other_game[0], "curso-b")
    with pytest.raises(ValidationError) as error:
        module.full_clean()
    assert "course" in error.value.message_dict


def test_no_se_mueve_una_leccion_probada_a_un_modulo_de_otro_juego(tested_lesson, other_game):
    other_course = make_course(other_game[0], "curso-b")
    tested_lesson.module = Module.objects.create(course=other_course, title="Otro", order=1)
    with pytest.raises(ValidationError) as error:
        tested_lesson.full_clean()
    assert "module" in error.value.message_dict


def test_se_mueve_una_leccion_probada_dentro_del_mismo_juego(tested_lesson, game):
    other_course = make_course(game[0], "curso-c")
    tested_lesson.module = Module.objects.create(course=other_course, title="Otro", order=1)
    tested_lesson.full_clean()


def test_no_se_borra_una_version_o_entorno_con_lecciones_probadas(tested_lesson, game):
    _, version, environment = game
    with pytest.raises(ProtectedError):
        version.delete()
    with pytest.raises(ProtectedError):
        environment.delete()


def lesson_form_data(module, version, environment, **overrides):
    data = {
        "module": module.pk,
        "title": "Lección desde el admin",
        "content": "# Hola",
        "estimated_minutes": 20,
        "order": 1,
        "status": Lesson.Status.PUBLISHED,
        "tests-TOTAL_FORMS": 1,
        "tests-INITIAL_FORMS": 0,
        "tests-MIN_NUM_FORMS": 0,
        "tests-MAX_NUM_FORMS": 1000,
        "tests-0-game_version": version.pk,
        "tests-0-modding_environment": environment.pk,
        "tests-0-tested_on": "2026-11-02",
    }
    return data | overrides


def test_administrador_crea_leccion_con_probado_con(admin_client, module, game):
    _, version, environment = game
    response = admin_client.post(
        reverse("admin:courses_lesson_add"), lesson_form_data(module, version, environment)
    )
    assert response.status_code == 302
    lesson = Lesson.objects.get(title="Lección desde el admin")
    assert lesson.module == module
    test = lesson.tests.get()
    assert (test.game_version, test.modding_environment) == (version, environment)


def test_admin_rechaza_probado_con_de_otro_juego(admin_client, module, other_game):
    _, other_version, other_environment = other_game
    response = admin_client.post(
        reverse("admin:courses_lesson_add"),
        lesson_form_data(module, other_version, other_environment),
    )
    assert response.status_code == 200
    errors = response.context["inline_admin_formsets"][0].formset.errors[0]
    assert set(errors) == {"game_version", "modding_environment"}
    assert not Lesson.objects.exists()


def test_administrador_agrega_modulos_desde_el_curso(admin_client, module):
    course = module.course
    response = admin_client.post(
        reverse("admin:courses_course_change", args=[course.pk]),
        {
            "title": course.title,
            "slug": course.slug,
            "game": course.game_id,
            "kind": course.kind,
            "level": course.level,
            "description": course.description,
            "requirements": course.requirements,
            "duration_weeks": course.duration_weeks,
            "price_cents": course.price_cents,
            "access_days": course.access_days,
            "status": course.status,
            "modules-TOTAL_FORMS": 2,
            "modules-INITIAL_FORMS": 1,
            "modules-MIN_NUM_FORMS": 0,
            "modules-MAX_NUM_FORMS": 1000,
            "modules-0-id": module.pk,
            "modules-0-course": course.pk,
            "modules-0-order": 1,
            "modules-0-title": module.title,
            "modules-1-course": course.pk,
            "modules-1-order": 2,
            "modules-1-title": "Semana 2",
        },
    )
    assert response.status_code == 302
    assert [m.title for m in course.modules.all()] == ["Semana 1", "Semana 2"]


@pytest.mark.parametrize("user_kind", ["anonimo", "alumno", "tutor"])
def test_sin_acceso_al_admin_no_se_puede_crear_leccion(client, module, game, user_kind):
    if user_kind != "anonimo":
        user = get_user_model().objects.create_user(
            email=f"{user_kind}@example.com",
            display_name=user_kind,
            is_tutor=user_kind == "tutor",
        )
        client.force_login(user)
    _, version, environment = game
    response = client.post(
        reverse("admin:courses_lesson_add"), lesson_form_data(module, version, environment)
    )
    assert response.status_code == 302
    assert not Lesson.objects.exists()
