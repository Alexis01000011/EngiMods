from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from courses.models import Course, Exercise, Lesson
from enrollments.models import Enrollment

from .forms import SubmissionAttemptForm
from .models import Submission


def find_submission(user, exercise, enrollment):
    """La entrega de la inscripción vigente o, si no hay, la más reciente del alumno."""
    submissions = Submission.objects.filter(exercise=exercise, enrollment__user=user)
    if enrollment is not None:
        return submissions.filter(enrollment=enrollment).first()
    return submissions.order_by("-created_at", "-pk").first()


@login_required
def submit(request, lesson_pk):
    """Página del ejercicio de una lección: formulario de entrega o estado de la entrega."""
    exercise = get_object_or_404(
        Exercise.objects.select_related("lesson__module__course__game"),
        lesson_id=lesson_pk,
        lesson__status=Lesson.Status.PUBLISHED,
        lesson__module__course__status=Course.Status.PUBLISHED,
    )
    course = exercise.lesson.module.course
    enrollment = Enrollment.objects.with_access().filter(user=request.user, course=course).first()
    submission = find_submission(request.user, exercise, enrollment)
    if enrollment is None and submission is None:
        raise PermissionDenied(_("No tienes acceso vigente a este curso."))

    form = None
    # Reenviar una entrega después de cambios es EM-073; aquí solo se envía la primera vez.
    if submission is None:
        form = SubmissionAttemptForm(request.POST or None, game=course.game)
        if request.method == "POST" and form.is_valid():
            with transaction.atomic():
                submission = Submission(exercise=exercise, enrollment=enrollment)
                submission.full_clean()
                submission.save()
                attempt = form.save(commit=False)
                attempt.submission = submission
                attempt.full_clean()
                attempt.save()
            return redirect("submissions:submit", lesson_pk)
    elif request.method == "POST":
        return redirect("submissions:submit", lesson_pk)

    attempt = (
        submission.attempts.select_related("game_version", "modding_environment").first()
        if submission
        else None
    )
    return render(
        request,
        "submissions/submit.html",
        {
            "course": course,
            "exercise": exercise,
            "form": form,
            "submission": submission,
            "attempt": attempt,
        },
    )


@login_required
def my_submissions(request):
    """Las entregas del alumno con su estado, solo las propias."""
    submissions = (
        Submission.objects.filter(enrollment__user=request.user)
        .select_related("exercise__lesson__module__course")
        .order_by("-created_at", "-pk")
    )
    return render(request, "submissions/my_submissions.html", {"submissions": submissions})
