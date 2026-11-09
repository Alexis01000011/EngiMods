from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _

from accounts.permissions import has_tutor_access
from catalog.models import Game
from core.views import latest_tests
from enrollments.models import Enrollment, LessonProgress

from .models import Course, Exercise, Lesson, Module


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.published().select_related("game"), slug=slug)
    lessons = Prefetch("lessons", queryset=Lesson.objects.published().order_by("order", "pk"))
    modules = list(
        Module.objects.filter(course=course).order_by("order", "pk").prefetch_related(lessons)
    )
    # Número de cada lección en el temario (01, 02…), igual que en la pantalla de la lección.
    number = 0
    for module in modules:
        for lesson in module.lessons.all():
            number += 1
            lesson.number = number
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
            # Quien ya tiene acceso vigente no ve el botón de pago (EM-042).
            "has_access": request.user.is_authenticated
            and Enrollment.objects.with_access().filter(user=request.user, course=course).exists(),
        },
    )


def can_view_lesson(user, course):
    """Alumno con acceso vigente a este curso, tutor o administrador."""
    if has_tutor_access(user):
        return True
    return Enrollment.objects.with_access().filter(user=user, course=course).exists()


@login_required
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
    if not can_view_lesson(request.user, course):
        raise PermissionDenied(_("No tienes acceso a esta lección."))
    lesson = lessons[position]
    # El botón de completada solo aparece a quien tiene inscripción vigente (no a tutores).
    enrollment = Enrollment.objects.with_access().filter(user=request.user, course=course).first()
    # Lecciones que el alumno ya completó, para el temario y su avance.
    completed_ids = set()
    if enrollment is not None:
        completed_ids = set(
            LessonProgress.objects.filter(enrollment=enrollment).values_list("lesson_id", flat=True)
        )
    completed = lesson.pk in completed_ids
    # Si hay varias pruebas, se muestra la más reciente por fecha de prueba.
    test = (
        lesson.tests.select_related("game_version__game", "modding_environment")
        .order_by("-tested_on", "-pk")
        .first()
    )
    exercise = Exercise.objects.filter(lesson=lesson).first()
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
            "enrollment": enrollment,
            "completed": completed,
            "exercise": exercise,
            "submission": submission,
            "lessons": lessons,
            "completed_ids": completed_ids,
            "completed_count": sum(1 for item in lessons if item.pk in completed_ids),
            "previous_lesson": lessons[position - 1] if position > 0 else None,
            "next_lesson": lessons[position + 1] if position < len(lessons) - 1 else None,
        },
    )
