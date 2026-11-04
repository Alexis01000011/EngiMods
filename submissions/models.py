from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import validate_git_repository_url


class Submission(models.Model):
    """Entrega de un ejercicio por parte de una inscripción. Sus envíos son SubmissionAttempt."""

    class Status(models.TextChoices):
        SUBMITTED = "submitted", _("Enviada")
        IN_REVIEW = "in_review", _("En revisión")
        APPROVED = "approved", _("Aprobada")
        CHANGES_REQUESTED = "changes_requested", _("Requiere cambios")

    # PROTECT: el historial de entregas no se borra al borrar un ejercicio o una inscripción.
    exercise = models.ForeignKey(
        "courses.Exercise",
        on_delete=models.PROTECT,
        related_name="submissions",
        verbose_name=_("ejercicio"),
    )
    enrollment = models.ForeignKey(
        "enrollments.Enrollment",
        on_delete=models.PROTECT,
        related_name="submissions",
        verbose_name=_("inscripción"),
    )
    status = models.CharField(_("estado"), max_length=20, choices=Status, default=Status.SUBMITTED)
    created_at = models.DateTimeField(_("fecha de creación"), default=timezone.now)

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = _("entrega")
        verbose_name_plural = _("entregas")
        constraints = [
            models.UniqueConstraint(
                fields=("exercise", "enrollment"), name="unique_submission_per_enrollment"
            )
        ]

    def __str__(self):
        return f"{self.enrollment.user} · {self.exercise}"

    def clean(self):
        super().clean()
        if self.exercise_id and self.enrollment_id:
            if self.exercise.lesson.module.course_id != self.enrollment.course_id:
                raise ValidationError(
                    {"exercise": _("El ejercicio no es del curso de la inscripción.")}
                )


class SubmissionAttempt(models.Model):
    """Un envío de una entrega: enlace al repositorio, comentario y con qué versión se hizo."""

    submission = models.ForeignKey(
        Submission,
        on_delete=models.PROTECT,
        related_name="attempts",
        verbose_name=_("entrega"),
    )
    repository_url = models.URLField(
        _("enlace al repositorio Git"),
        max_length=500,
        validators=[validate_git_repository_url],
    )
    comment = models.TextField(_("comentario"), blank=True)
    game_version = models.ForeignKey(
        "catalog.GameVersion",
        on_delete=models.PROTECT,
        related_name="submission_attempts",
        verbose_name=_("versión del juego"),
    )
    modding_environment = models.ForeignKey(
        "catalog.ModdingEnvironment",
        on_delete=models.PROTECT,
        related_name="submission_attempts",
        verbose_name=_("entorno de modding"),
    )
    submitted_at = models.DateTimeField(_("fecha de envío"), default=timezone.now)
    # Quién tomó la revisión de este envío y cuándo (EM-071). Un reenvío (EM-073) es otro envío.
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reviewed_attempts",
        verbose_name=_("tutor que revisa"),
    )
    review_started_at = models.DateTimeField(_("inicio de la revisión"), null=True, blank=True)

    class Meta:
        ordering = ("-submitted_at", "-pk")
        verbose_name = _("envío")
        verbose_name_plural = _("envíos")

    def __str__(self):
        return f"{self.submission} · {self.submitted_at:%Y-%m-%d %H:%M}"

    def clean(self):
        super().clean()
        if not self.submission_id:
            return
        game_id = self.submission.exercise.lesson.module.course.game_id
        errors = {}
        if self.game_version_id and self.game_version.game_id != game_id:
            errors["game_version"] = _("La versión no es del juego del curso.")
        if self.modding_environment_id and self.modding_environment.game_id != game_id:
            errors["modding_environment"] = _("El entorno no es del juego del curso.")
        if errors:
            raise ValidationError(errors)


class ReviewQuerySet(models.QuerySet):
    def with_scores(self):
        """Con el tutor y la calificación de cada criterio, para mostrar la revisión completa."""
        return self.select_related("reviewer").prefetch_related(
            models.Prefetch("scores", ReviewScore.objects.select_related("criterion"))
        )


class Review(models.Model):
    """Revisión de un envío con rúbrica, comentario general y decisión (EM-072)."""

    # La decisión es uno de los dos estados finales de la entrega.
    class Decision(models.TextChoices):
        APPROVED = Submission.Status.APPROVED.value, Submission.Status.APPROVED.label
        CHANGES_REQUESTED = (
            Submission.Status.CHANGES_REQUESTED.value,
            Submission.Status.CHANGES_REQUESTED.label,
        )

    attempt = models.OneToOneField(
        SubmissionAttempt,
        on_delete=models.PROTECT,
        related_name="review",
        verbose_name=_("envío"),
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reviews",
        verbose_name=_("tutor"),
    )
    decision = models.CharField(_("decisión"), max_length=20, choices=Decision)
    comment = models.TextField(_("comentario general"))
    reviewed_at = models.DateTimeField(_("fecha de revisión"), default=timezone.now)

    objects = ReviewQuerySet.as_manager()

    class Meta:
        ordering = ("-reviewed_at", "-pk")
        verbose_name = _("revisión")
        verbose_name_plural = _("revisiones")

    def __str__(self):
        return f"{self.attempt} · {self.get_decision_display()}"


class ReviewScore(models.Model):
    """Calificación de un criterio de la rúbrica dentro de una revisión."""

    class Level(models.TextChoices):
        MEETS = "meets", _("Cumple")
        PARTIAL = "partial", _("Cumple en parte")
        NOT_YET = "not_yet", _("Aún no cumple")

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="scores", verbose_name=_("revisión")
    )
    # PROTECT: un criterio ya calificado no se borra, para no perder la revisión.
    criterion = models.ForeignKey(
        "courses.RubricCriterion",
        on_delete=models.PROTECT,
        related_name="scores",
        verbose_name=_("criterio"),
    )
    level = models.CharField(_("calificación"), max_length=20, choices=Level)

    class Meta:
        ordering = ("criterion__order", "criterion__pk")
        verbose_name = _("calificación por criterio")
        verbose_name_plural = _("calificaciones por criterio")
        constraints = [
            models.UniqueConstraint(
                fields=("review", "criterion"), name="unique_score_per_criterion"
            )
        ]

    def __str__(self):
        return f"{self.criterion.title} · {self.get_level_display()}"

    def clean(self):
        super().clean()
        if self.review_id and self.criterion_id:
            if self.criterion.exercise_id != self.review.attempt.submission.exercise_id:
                raise ValidationError(
                    {"criterion": _("El criterio no es de la rúbrica de este ejercicio.")}
                )
