from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _

from accounts.permissions import has_tutor_access
from catalog.models import Game
from enrollments.models import Enrollment, LessonProgress

from .models import Course, Lesson, Module


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.published().select_related("game"), slug=slug)
    lessons = Prefetch("lessons", queryset=Lesson.objects.published().order_by("order", "pk"))
    modules = Module.objects.filter(course=course).order_by("order", "pk").prefetch_related(lessons)
    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            # Un juego oculto no tiene página pública; no se enlaza.
            "game_is_public": course.game.status == Game.Status.ACTIVE,
            "modules": modules,
            "price": Decimal(course.price_cents) / 100,
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
    position = next((i for i, item in enumerate(lessons) if item.pk == pk), None)
    if position is None:
        raise Http404
    if not can_view_lesson(request.user, course):
        raise PermissionDenied(_("No tienes acceso a esta lección."))
    lesson = lessons[position]
    # El botón de completada solo aparece a quien tiene inscripción vigente (no a tutores).
    enrollment = Enrollment.objects.with_access().filter(user=request.user, course=course).first()
    completed = (
        enrollment is not None
        and LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).exists()
    )
    # Si hay varias pruebas, se muestra la más reciente por fecha de prueba.
    test = (
        lesson.tests.select_related("game_version__game", "modding_environment")
        .order_by("-tested_on", "-pk")
        .first()
    )
    return render(
        request,
        "courses/lesson_detail.html",
        {
            "course": course,
            "lesson": lesson,
            "test": test,
            "enrollment": enrollment,
            "completed": completed,
            "previous_lesson": lessons[position - 1] if position > 0 else None,
            "next_lesson": lessons[position + 1] if position < len(lessons) - 1 else None,
        },
    )
