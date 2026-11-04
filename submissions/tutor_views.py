"""Pantallas del tutor para revisar entregas, fuera del admin (EM-071 y EM-072)."""

from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Max, Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.permissions import tutor_required

from .forms import ReviewForm
from .models import Review, ReviewScore, Submission, SubmissionAttempt

PENDING = (Submission.Status.SUBMITTED, Submission.Status.IN_REVIEW)


def latest_attempts():
    return Prefetch(
        "attempts",
        queryset=SubmissionAttempt.objects.select_related(
            "reviewer", "game_version", "modding_environment"
        ).order_by("-submitted_at", "-pk"),
    )


@tutor_required
def queue(request):
    """Entregas pendientes, de la más vieja a la más nueva.

    Mientras no haya grupos (EM-050), todos los tutores ven todas.
    """
    deadline = timedelta(hours=settings.REVIEW_DEADLINE_HOURS)
    now = timezone.now()
    submissions = list(
        Submission.objects.filter(status__in=PENDING)
        .annotate(last_submitted_at=Max("attempts__submitted_at"))
        .filter(last_submitted_at__isnull=False)
        .select_related("enrollment__user", "enrollment__course", "exercise__lesson")
        .prefetch_related(latest_attempts())
        .order_by("last_submitted_at", "pk")
    )
    for submission in submissions:
        submission.attempt = submission.attempts.all()[0]
        submission.overdue = now - submission.last_submitted_at > deadline
        submission.due_at = submission.last_submitted_at + deadline
    return render(
        request,
        "submissions/tutor_queue.html",
        {"submissions": submissions, "deadline_hours": settings.REVIEW_DEADLINE_HOURS},
    )


@tutor_required
def review(request, pk):
    """Detalle de una entrega. Quien tomó la revisión la califica con la rúbrica (EM-072)."""
    submission = get_object_or_404(
        Submission.objects.select_related(
            "enrollment__user", "enrollment__course", "exercise__lesson"
        ).prefetch_related(latest_attempts()),
        pk=pk,
    )
    attempt = submission.attempts.all()[0] if submission.attempts.all() else None
    criteria = list(submission.exercise.rubric_criteria.all())
    can_review = (
        submission.status == Submission.Status.IN_REVIEW
        and attempt is not None
        and attempt.reviewer_id == request.user.pk
    )
    form = None
    if can_review:
        data = request.POST if request.method == "POST" else None
        form = ReviewForm(data, criteria=criteria)
        if request.method == "POST" and form.is_valid():
            if save_review(submission.pk, request.user, form):
                messages.success(
                    request, _("Listo. Guardamos la revisión y el alumno ya puede verla.")
                )
                return redirect("reviews:queue")
            return redirect("reviews:review", pk)
    elif request.method == "POST":
        raise PermissionDenied(_("Solo el tutor que tomó la revisión puede enviarla."))

    return render(
        request,
        "submissions/tutor_review.html",
        {
            "submission": submission,
            "attempt": attempt,
            "criteria": criteria,
            "form": form,
            "review": Review.objects.with_scores().filter(attempt=attempt).first()
            if attempt
            else None,
        },
    )


def save_review(submission_pk, reviewer, form):
    """Guarda la revisión y cierra la entrega con la decisión. False si alguien se adelantó."""
    with transaction.atomic():
        submission = Submission.objects.select_for_update().get(pk=submission_pk)
        attempt = submission.attempts.order_by("-submitted_at", "-pk").first()
        if (
            submission.status != Submission.Status.IN_REVIEW
            or attempt is None
            or attempt.reviewer_id != reviewer.pk
            or Review.objects.filter(attempt=attempt).exists()
        ):
            return False
        review = Review(
            attempt=attempt,
            reviewer=reviewer,
            decision=form.cleaned_data["decision"],
            comment=form.cleaned_data["comment"],
        )
        review.full_clean()
        review.save()
        for criterion, level in form.scores():
            score = ReviewScore(review=review, criterion=criterion, level=level)
            score.full_clean()
            score.save()
        submission.status = review.decision
        submission.save(update_fields=["status"])
    return True


@tutor_required
@require_POST
def start_review(request, pk):
    """Toma la revisión: la entrega pasa a en revisión y queda registrado quién y cuándo."""
    with transaction.atomic():
        submission = get_object_or_404(Submission.objects.select_for_update(), pk=pk)
        attempt = submission.attempts.order_by("-submitted_at", "-pk").first()
        # Si otro tutor ya la tomó, se respeta: no se reasigna.
        if submission.status == Submission.Status.SUBMITTED and attempt is not None:
            submission.status = Submission.Status.IN_REVIEW
            submission.save(update_fields=["status"])
            attempt.reviewer = request.user
            attempt.review_started_at = timezone.now()
            attempt.save(update_fields=["reviewer", "review_started_at"])
    return redirect("reviews:review", pk)
