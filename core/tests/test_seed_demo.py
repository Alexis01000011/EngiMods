"""Datos de ejemplo para desarrollo (EM-006)."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonTest, Module

pytestmark = pytest.mark.django_db


def seed():
    call_command("seed_demo", verbosity=0)


def test_crea_dos_juegos_con_versiones_y_entornos():
    seed()

    assert Game.objects.count() == 2
    assert GameVersion.objects.count() == 2
    assert ModdingEnvironment.objects.count() == 2
    for game in Game.objects.all():
        assert game.status == Game.Status.ACTIVE
        version = game.versions.get()
        assert version.is_current
        assert game.modding_environments.get().compatible_versions.filter(pk=version.pk).exists()


def test_crea_un_curso_publicado_por_juego_con_modulos_y_lecciones():
    seed()

    assert Course.objects.count() == 2
    for course in Course.objects.all():
        assert course.status == Course.Status.PUBLISHED
        assert course.modules.count() == 2
        assert Lesson.objects.filter(module__course=course).count() == 4


def test_cada_leccion_tiene_su_prueba_y_hay_una_de_muestra_por_curso():
    seed()

    assert Lesson.objects.count() == 8
    assert LessonTest.objects.count() == 8
    for course in Course.objects.all():
        lessons = Lesson.objects.filter(module__course=course)
        assert lessons.filter(is_sample=True).count() == 1
        assert LessonTest.objects.filter(lesson__in=lessons).count() == lessons.count()


def test_crea_un_tutor_y_dos_alumnos_con_correo_verificado():
    seed()

    users = get_user_model().objects.filter(email__endswith="@example.com")
    assert users.count() == 3
    assert users.filter(is_tutor=True).count() == 1
    assert users.filter(is_tutor=False).count() == 2
    assert all(user.email_verified_at is not None for user in users)
    assert all(user.check_password("demo12345") for user in users)


def test_se_puede_correr_varias_veces_sin_duplicar_datos():
    seed()
    counts = (
        Game.objects.count(),
        GameVersion.objects.count(),
        ModdingEnvironment.objects.count(),
        Course.objects.count(),
        Module.objects.count(),
        Lesson.objects.count(),
        LessonTest.objects.count(),
        get_user_model().objects.count(),
    )

    seed()

    assert counts == (
        Game.objects.count(),
        GameVersion.objects.count(),
        ModdingEnvironment.objects.count(),
        Course.objects.count(),
        Module.objects.count(),
        Lesson.objects.count(),
        LessonTest.objects.count(),
        get_user_model().objects.count(),
    )
