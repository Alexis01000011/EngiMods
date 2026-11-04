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
