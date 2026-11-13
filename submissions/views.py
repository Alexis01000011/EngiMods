from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from courses.models import Course, Exercise, Lesson
from enrollments.models import Enrollment

from .forms import SubmissionAttemptForm
from .models import Review, Submission


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

    attempts = attempts_with_reviews(submission) if submission else []
    attempt = attempts[0] if attempts else None
    # Reenvío (EM-073): solo si el tutor pidió cambios y la inscripción de la entrega sigue vigente.
    can_resubmit = (
        submission is not None
        and submission.status == Submission.Status.CHANGES_REQUESTED
        and enrollment is not None
    )

    form = None
    if submission is None or can_resubmit:
        initial = None
        if attempt is not None:
            initial = {
                "repository_url": attempt.repository_url,
                "game_version": attempt.game_version_id,
                "modding_environment": attempt.modding_environment_id,
            }
        form = SubmissionAttemptForm(request.POST or None, game=course.game, initial=initial)
        if request.method == "POST" and form.is_valid():
            if submission is None:
                create_submission(exercise, enrollment, form)
            else:
                resubmit(submission.pk, form)
            return redirect("submissions:submit", lesson_pk)
    elif request.method == "POST":
        return redirect("submissions:submit", lesson_pk)

    return render(
        request,
        "submissions/submit.html",
        {
            "course": course,
            "exercise": exercise,
            "form": form,
            "submission": submission,
            "attempt": attempt,
            # La revisión del tutor, con su rúbrica (EM-072). Solo de la entrega propia.
            "review": attempt.past_review if attempt else None,
            "previous_attempts": attempts[1:],
            "review_hours": settings.REVIEW_DEADLINE_HOURS,
        },
    )


def attempts_with_reviews(submission):
    """Los envíos de la entrega, del más nuevo al más viejo, con su número y su revisión."""
    attempts = list(
        submission.attempts.select_related(
            "reviewer", "game_version", "modding_environment"
        ).order_by("-submitted_at", "-pk")
    )
    reviews = {
        review.attempt_id: review
        for review in Review.objects.with_scores().filter(attempt__in=attempts)
    }
    for index, attempt in enumerate(attempts):
        attempt.number = len(attempts) - index
        attempt.past_review = reviews.get(attempt.pk)
    return attempts


def create_submission(exercise, enrollment, form):
    with transaction.atomic():
        submission = Submission(exercise=exercise, enrollment=enrollment)
        submission.full_clean()
        submission.save()
        save_attempt(submission, form)


def resubmit(submission_pk, form):
    """Agrega un envío nuevo y la entrega vuelve a la cola. Los anteriores no se tocan."""
    with transaction.atomic():
        submission = Submission.objects.select_for_update().get(pk=submission_pk)
        # Si dos envíos llegan juntos, solo cuenta el primero.
        if submission.status != Submission.Status.CHANGES_REQUESTED:
            return
        save_attempt(submission, form)
        submission.status = Submission.Status.SUBMITTED
        submission.save(update_fields=["status"])


def save_attempt(submission, form):
    attempt = form.save(commit=False)
    attempt.submission = submission
    attempt.full_clean()
    attempt.save()


@login_required
def my_submissions(request):
    """Las entregas del alumno con su estado, solo las propias."""
    submissions = (
        Submission.objects.filter(enrollment__user=request.user)
        .select_related("exercise__lesson__module__course")
        .order_by("-created_at", "-pk")
    )
    return render(request, "submissions/my_submissions.html", {"submissions": submissions})
