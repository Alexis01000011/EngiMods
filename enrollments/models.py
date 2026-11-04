from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EnrollmentQuerySet(models.QuerySet):
    def with_access(self):
        """Inscripciones con acceso vigente: activas y con fecha de fin de acceso en el futuro."""
        return self.filter(status=Enrollment.Status.ACTIVE, access_ends_at__gt=timezone.now())


class Enrollment(models.Model):
    """Inscripción de un alumno a un curso. La usan el admin (manual) y el webhook de Stripe."""

    class Origin(models.TextChoices):
        STRIPE = "stripe", _("Stripe")
        SCHOLARSHIP = "scholarship", _("Beca")
        TRIAL = "trial", _("Prueba")
        EXTERNAL_PAYMENT = "external_payment", _("Pago externo")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Activa")
        CANCELLED = "cancelled", _("Cancelada")

    # PROTECT: no se borra un alumno ni un curso con inscripciones.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name=_("alumno"),
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name=_("curso"),
    )
    origin = models.CharField(_("origen"), max_length=20, choices=Origin)
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.ACTIVE)
    enrolled_at = models.DateTimeField(_("fecha de inscripción"), default=timezone.now)
    access_ends_at = models.DateTimeField(
        _("fin de acceso"),
        blank=True,
        help_text=_(
            "Si se deja vacío, se calcula con los días de acceso del curso a partir de la "
            "fecha de inscripción."
        ),
    )

    objects = EnrollmentQuerySet.as_manager()

    class Meta:
        ordering = ("-enrolled_at", "-pk")
        verbose_name = _("inscripción")
        verbose_name_plural = _("inscripciones")

    def __str__(self):
        return f"{self.user} · {self.course}"

    def save(self, *args, **kwargs):
        # Quien cree inscripciones sin pasar por un formulario (como el webhook) recibe la
        # fecha de fin calculada; la regla de no duplicar vigentes está en clean().
        self._fill_access_ends_at()
        super().save(*args, **kwargs)

    @property
    def has_access(self):
        """Acceso vigente: inscripción activa que no ha pasado su fecha de fin de acceso."""
        return (
            self.status == self.Status.ACTIVE
            and self.access_ends_at is not None
            and self.access_ends_at > timezone.now()
        )

    @property
    def is_expired(self):
        """Vencida se calcula; no se guarda como estado."""
        return (
            self.status == self.Status.ACTIVE
            and self.access_ends_at is not None
            and self.access_ends_at <= timezone.now()
        )

    def _fill_access_ends_at(self):
        if self.access_ends_at is None and self.course_id and self.enrolled_at:
            self.access_ends_at = self.enrolled_at + timedelta(days=self.course.access_days)

    def clean(self):
        super().clean()
        self._fill_access_ends_at()
        if self.user_id and self.course_id and self.has_access:
            others = Enrollment.objects.with_access().filter(
                user_id=self.user_id, course_id=self.course_id
            )
            if others.exclude(pk=self.pk).exists():
                raise ValidationError(
                    _("El alumno ya tiene una inscripción con acceso vigente a este curso.")
                )


class LessonProgress(models.Model):
    """Lección que el alumno marcó como completada dentro de una inscripción."""

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
        verbose_name=_("inscripción"),
    )
    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="progress",
        verbose_name=_("lección"),
    )
    completed_at = models.DateTimeField(_("fecha de completado"), default=timezone.now)

    class Meta:
        ordering = ("-completed_at", "-pk")
        verbose_name = _("lección completada")
        verbose_name_plural = _("lecciones completadas")
        constraints = [
            models.UniqueConstraint(
                fields=("enrollment", "lesson"), name="unique_lesson_progress_per_enrollment"
            )
        ]

    def __str__(self):
        return f"{self.enrollment} · {self.lesson}"
