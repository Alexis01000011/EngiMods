from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from courses.models import Course, Lesson

from .models import Enrollment, LessonProgress


def course_lessons(course):
    """Lecciones publicadas del curso, en el mismo orden que la navegación entre lecciones."""
    return list(
        Lesson.objects.published()
        .filter(module__course=course)
        .order_by("module__order", "module__pk", "order", "pk")
    )


def add_progress(enrollment):
    """Agrega a la inscripción su porcentaje de avance y la siguiente lección pendiente."""
    lessons = course_lessons(enrollment.course)
    done = set(enrollment.lesson_progress.values_list("lesson_id", flat=True))
    completed = sum(1 for lesson in lessons if lesson.pk in done)
    enrollment.completed_count = completed
    enrollment.lesson_count = len(lessons)
    # Se redondea hacia abajo: 100 % solo cuando están todas.
    enrollment.progress_percent = completed * 100 // len(lessons) if lessons else 0
    enrollment.all_done = bool(lessons) and completed == len(lessons)
    enrollment.has_lessons = bool(lessons)
    # Si el curso volvió a borrador, sus lecciones dan 404: no se enlaza ninguna.
    enrollment.next_lesson = None
    if enrollment.course.status == Course.Status.PUBLISHED:
        enrollment.next_lesson = next((item for item in lessons if item.pk not in done), None)


@login_required
def my_courses(request):
    """Panel del alumno: sus cursos con acceso vigente y los vencidos, solo los propios."""
    enrollments = Enrollment.objects.filter(
        user=request.user, status=Enrollment.Status.ACTIVE
    ).select_related("course__game")
    active = list(enrollments.with_access().order_by("-enrolled_at", "-pk"))

    # Un curso con una inscripción vigente no aparece también como vencido, ni se repite.
    expired = []
    seen = {enrollment.course_id for enrollment in active}
    for enrollment in enrollments.filter(access_ends_at__lte=timezone.now()).order_by(
        "-access_ends_at", "-pk"
    ):
        if enrollment.course_id not in seen:
            seen.add(enrollment.course_id)
            expired.append(enrollment)

    for enrollment in active + expired:
        add_progress(enrollment)

    catalog = []
    if not active and not expired:
        catalog = Course.objects.published().select_related("game").order_by("title")
    return render(
        request,
        "enrollments/my_courses.html",
        {"active": active, "expired": expired, "catalog": catalog},
    )


@login_required
@require_POST
def toggle_lesson(request, pk):
    """Marca o desmarca una lección como completada. Solo con acceso vigente al curso."""
    lesson = get_object_or_404(
        Lesson.objects.published().select_related("module__course"),
        pk=pk,
        module__course__status=Course.Status.PUBLISHED,
    )
    course = lesson.module.course
    enrollment = Enrollment.objects.with_access().filter(user=request.user, course=course).first()
    if enrollment is None:
        raise PermissionDenied(_("No tienes acceso vigente a este curso."))
    deleted, _deleted = LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).delete()
    if not deleted:
        LessonProgress.objects.create(enrollment=enrollment, lesson=lesson)
    return redirect("courses:lesson_detail", course.slug, lesson.pk)
