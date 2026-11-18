from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from courses.models import Course


class Cohort(models.Model):
    """Grupo de un curso por grupos: fechas, cupo, tutores y enlace de Discord (EM-050)."""

    class Status(models.TextChoices):
        OPEN = "open", _("Inscripción abierta")
        RUNNING = "running", _("En curso")
        CLOSED = "closed", _("Cerrado")

    # PROTECT: no se borra un curso con grupos.
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.PROTECT,
        related_name="cohorts",
        verbose_name=_("curso"),
    )
    name = models.CharField(_("nombre"), max_length=150)
    start_date = models.DateField(_("fecha de inicio"))
    end_date = models.DateField(_("fecha de fin"))
    capacity = models.PositiveSmallIntegerField(_("cupo"), validators=[MinValueValidator(1)])
    tutors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="cohorts",
        verbose_name=_("tutores"),
    )
    discord_url = models.URLField(_("enlace de Discord"), blank=True)
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.OPEN)

    class Meta:
        ordering = ("-start_date", "course__title", "name")
        verbose_name = _("grupo")
        verbose_name_plural = _("grupos")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "name"), name="cohorts_unique_name_per_course"
            ),
        ]

    def __str__(self):
        return f"{self.course} · {self.name}"

    def clean(self):
        super().clean()
        errors = {}
        if self.course_id and self.course.kind != Course.Kind.COURSE:
            errors["course"] = _(
                "Solo los cursos de tipo curso tienen grupos; las prácticas son autoguiadas."
            )
        if self.start_date and self.end_date and self.end_date < self.start_date:
            errors["end_date"] = _("La fecha de fin no puede ser anterior a la de inicio.")
        if errors:
            raise ValidationError(errors)

    @property
    def seats_taken(self):
        from enrollments.models import Enrollment

        return self.enrollments.filter(status=Enrollment.Status.ACTIVE).count()

    @property
    def seats_left(self):
        return max(self.capacity - self.seats_taken, 0)

    @property
    def is_full(self):
        return self.seats_taken >= self.capacity


class LiveSession(models.Model):
    """Clínica en vivo de un grupo: fecha, hora de México, tema y enlace (EM-052)."""

    cohort = models.ForeignKey(
        Cohort, on_delete=models.CASCADE, related_name="live_sessions", verbose_name=_("grupo")
    )
    date = models.DateField(_("fecha"))
    start_time = models.TimeField(_("hora"))
    topic = models.CharField(_("tema"), max_length=200)
    join_url = models.URLField(_("enlace para entrar"), max_length=500)

    class Meta:
        ordering = ("date", "start_time", "pk")
        verbose_name = _("clínica en vivo")
        verbose_name_plural = _("clínicas en vivo")

    def __str__(self):
        return f"{self.cohort} · {self.topic}"

    @property
    def starts_at(self):
        """La fecha y hora se guardan en la zona de México (settings.TIME_ZONE)."""
        return timezone.make_aware(datetime.combine(self.date, self.start_time))

    @property
    def is_past(self):
        return self.starts_at < timezone.now()
