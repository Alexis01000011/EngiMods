"""Revalidación de lecciones cuando sale una versión nueva (EM-014)."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.permissions import tutor_required
from catalog.models import GameVersion

from .forms import RevalidationForm
from .models import Course, Lesson


def pending_lessons():
    """Lecciones publicadas probadas solo en versiones anteriores a la actual, por curso."""
    current = {version.game_id: version for version in GameVersion.objects.filter(is_current=True)}
    lessons = (
        Lesson.objects.published()
        .filter(module__course__status=Course.Status.PUBLISHED, tests__isnull=False)
        .select_related("module__course__game")
        .prefetch_related(
            "tests__game_version", "tests__modding_environment", "tests__game_version__game"
        )
        .order_by("module__course__title", "module__order", "order", "pk")
        .distinct()
    )
    groups = {}
    for lesson in lessons:
        version = current.get(lesson.module.course.game_id)
        if version is None:
            continue
        tests = list(lesson.tests.all())
        if any(test.game_version_id == version.pk for test in tests):
            continue
        latest = max(tests, key=lambda test: (test.tested_on, test.pk))
        lesson.latest_test = latest
        lesson.current_version = version
        lesson.form = RevalidationForm(
            game=lesson.module.course.game,
            initial={"game_version": version.pk},
        )
        group = groups.setdefault(
            lesson.module.course_id, {"course": lesson.module.course, "lessons": []}
        )
        group["lessons"].append(lesson)
    return list(groups.values())


@tutor_required
def queue(request):
    return render(
        request,
        "courses/revalidation_queue.html",
        {"groups": pending_lessons()},
    )


@tutor_required
@require_POST
def revalidate(request, pk):
    lesson = get_object_or_404(
        Lesson.objects.published().select_related("module__course__game"),
        pk=pk,
        module__course__status=Course.Status.PUBLISHED,
    )
    form = RevalidationForm(request.POST, game=lesson.module.course.game)
    if form.is_valid():
        test = form.save(commit=False)
        test.lesson = lesson
        test.full_clean()
        test.save()
        messages.success(
            request,
            _("Listo. Registramos la nueva prueba de %(lesson)s.") % {"lesson": lesson.title},
        )
    else:
        messages.error(
            request, _("No se pudo registrar la prueba. Revisa la versión, el entorno y la fecha.")
        )
    return redirect("revalidation:queue")
