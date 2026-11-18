from decimal import Decimal

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _

from accounts.permissions import has_tutor_access
from catalog.models import Game, GameVersion
from core.views import latest_tests
from enrollments.models import Enrollment, LessonProgress

from .models import Course, Exercise, Lesson, LessonResource, Module


def course_list(request):
    """Catálogo público de cursos (EM-013), con filtros por juego y nivel en la URL."""
    courses = (
        Course.objects.published()
        .filter(game__status=Game.Status.ACTIVE)
        .select_related("game")
        .order_by("title", "pk")
    )
    game_slug = request.GET.get("juego", "").strip()
    level = request.GET.get("nivel", "").strip()
    if game_slug:
        courses = courses.filter(game__slug=game_slug)
    if level in Course.Level.values:
        courses = courses.filter(level=level)
    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses,
            "games": Game.objects.filter(status=Game.Status.ACTIVE).order_by("name"),
            "levels": Course.Level.choices,
            "selected_game": game_slug,
            "selected_level": level,
        },
    )


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.published().select_related("game"), slug=slug)
    lessons = Prefetch("lessons", queryset=Lesson.objects.published().order_by("order", "pk"))
    modules = list(
        Module.objects.filter(course=course).order_by("order", "pk").prefetch_related(lessons)
    )
    # Número de cada lección en el temario (01, 02…), igual que en la pantalla de la lección.
    number = 0
    sample_lesson = None
    for module in modules:
        for lesson in module.lessons.all():
            number += 1
            lesson.number = number
            # La página del curso enlaza a la primera lección de muestra (EM-024).
            if sample_lesson is None and lesson.is_sample:
                sample_lesson = lesson
    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            # Un juego oculto no tiene página pública; no se enlaza.
            "game_is_public": course.game.status == Game.Status.ACTIVE,
            "modules": modules,
            "price": Decimal(course.price_cents) / 100,
            "latest_test": latest_tests([course]).get(course.pk),
            "sample_lesson": sample_lesson,
            # Quien ya tiene acceso vigente no ve el botón de pago (EM-042).
            "has_access": request.user.is_authenticated
            and Enrollment.objects.with_access().filter(user=request.user, course=course).exists(),
        },
    )


def can_view_lesson(user, course):
    """Alumno con acceso vigente a este curso, tutor o administrador."""
    if has_tutor_access(user):
        return True
    if not user.is_authenticated:
        return False
    return Enrollment.objects.with_access().filter(user=user, course=course).exists()


def lesson_detail(request, slug, pk):
    # Borradores (de la lección o del curso) y lecciones de otro curso responden 404 a todos.
    course = get_object_or_404(Course.objects.published(), slug=slug)
    lessons = list(
        Lesson.objects.published()
        .filter(module__course=course)
        .select_related("module")
        .order_by("module__order", "module__pk", "order", "pk")
    )
    for number, item in enumerate(lessons, start=1):
        item.number = number  # Número en el temario: 01, 02…
    position = next((i for i, item in enumerate(lessons) if item.pk == pk), None)
    if position is None:
        raise Http404
    lesson = lessons[position]
    has_access = can_view_lesson(request.user, course)
    if not has_access and not lesson.is_sample:
        # Las lecciones de muestra se ven sin cuenta ni pago (EM-024); las demás piden
        # sesión (y después acceso vigente al curso).
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        raise PermissionDenied(_("No tienes acceso a esta lección."))
    # El botón de completada solo aparece a quien tiene inscripción vigente (no a tutores).
    enrollment = None
    if request.user.is_authenticated:
        enrollment = (
            Enrollment.objects.with_access().filter(user=request.user, course=course).first()
        )
    # Lecciones que el alumno ya completó, para el temario y su avance.
    completed_ids = set()
    if enrollment is not None:
        completed_ids = set(
            LessonProgress.objects.filter(enrollment=enrollment).values_list("lesson_id", flat=True)
        )
    completed = lesson.pk in completed_ids
    # Si hay una prueba con la versión actual, se muestra esa; si no, la más reciente.
    tests = list(
        lesson.tests.select_related("game_version__game", "modding_environment").order_by(
            "-tested_on", "-pk"
        )
    )
    current_version = GameVersion.objects.filter(game=course.game, is_current=True).first()
    current_test = next(
        (
            item
            for item in tests
            if current_version is not None and item.game_version_id == current_version.pk
        ),
        None,
    )
    test = current_test or (tests[0] if tests else None)
    # Probada solo en versiones anteriores: hay que revalidarla con la actual (EM-014).
    needs_revalidation = bool(tests and current_version and current_test is None)
    exercise = Exercise.objects.filter(lesson=lesson).first()
    # Solo los alumnos con acceso ven los recursos; las lecciones de muestra los abren a todos.
    resources = []
    if lesson.is_sample or enrollment is not None:
        resources = LessonResource.objects.filter(lesson=lesson).select_related(
            "game_version__game", "modding_environment"
        )
    submission = None
    if exercise and enrollment:
        submission = exercise.submissions.filter(enrollment=enrollment).first()
    return render(
        request,
        "courses/lesson_detail.html",
        {
            "course": course,
            "lesson": lesson,
            "test": test,
            "current_version": current_version,
            "needs_revalidation": needs_revalidation,
            "enrollment": enrollment,
            "has_access": has_access,
            "completed": completed,
            "exercise": exercise,
            "resources": resources,
            "submission": submission,
            "lessons": lessons,
            "completed_ids": completed_ids,
            "completed_count": sum(1 for item in lessons if item.pk in completed_ids),
            "previous_lesson": lessons[position - 1] if position > 0 else None,
            "next_lesson": lessons[position + 1] if position < len(lessons) - 1 else None,
        },
    )
