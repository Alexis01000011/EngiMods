from datetime import datetime, time, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import LegalText
from courses.models import Course


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
    # Opcional: solo en cursos por grupos. PROTECT para no perder de qué grupo era.
    cohort = models.ForeignKey(
        "cohorts.Cohort",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="enrollments",
        verbose_name=_("grupo"),
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
        if self.access_ends_at is not None or not self.course_id or not self.enrolled_at:
            return
        if self.cohort_id:
            # En un curso por grupos, el acceso se cuenta desde que termina el grupo.
            base = timezone.make_aware(datetime.combine(self.cohort.end_date, time.max))
        else:
            base = self.enrolled_at
        self.access_ends_at = base + timedelta(days=self.course.access_days)

    def clean(self):
        super().clean()
        self._fill_access_ends_at()
        errors = {}
        if self.cohort_id and self.course_id:
            if self.cohort.course_id != self.course_id:
                errors["cohort"] = _("El grupo no es del curso de la inscripción.")
            elif self.course.kind != Course.Kind.COURSE:
                errors["cohort"] = _("Solo los cursos por grupos llevan grupo.")
            elif (
                self.cohort.enrollments.filter(status=self.Status.ACTIVE)
                .exclude(pk=self.pk)
                .count()
                >= self.cohort.capacity
            ):
                errors["cohort"] = _("El grupo ya está lleno.")
        if self.user_id and self.course_id and self.has_access:
            others = Enrollment.objects.with_access().filter(
                user_id=self.user_id, course_id=self.course_id
            )
            if others.exclude(pk=self.pk).exists():
                errors["__all__"] = _(
                    "El alumno ya tiene una inscripción con acceso vigente a este curso."
                )
        if errors:
            raise ValidationError(errors)


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


class WaitlistEntry(models.Model):
    """Interés de un visitante en un juego o en uno de sus cursos (EM-046).

    Se guarda sin cuenta. El consentimiento del aviso de privacidad vive en
    ``accounts.PrivacyConsent``, ligado al mismo correo.
    """

    email = models.EmailField(_("correo"))
    # PROTECT: el interés es dato de demanda; un juego o curso con lista de espera
    # se oculta, no se borra.
    game = models.ForeignKey(
        "catalog.Game",
        on_delete=models.PROTECT,
        related_name="waitlist_entries",
        verbose_name=_("juego"),
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.PROTECT,
        related_name="waitlist_entries",
        verbose_name=_("curso"),
        null=True,
        blank=True,
        help_text=_("Opcional. Si se elige, debe ser un curso del juego."),
    )
    legal_text = models.ForeignKey(
        LegalText,
        on_delete=models.PROTECT,
        related_name="waitlist_entries",
        verbose_name=_("aviso de privacidad aceptado"),
        limit_choices_to={"kind": LegalText.Kind.PRIVACY},
    )
    created_at = models.DateTimeField(_("registrado el"), auto_now_add=True)

    class Meta:
        ordering = ("game__name", "game__pk", "course__title", "-created_at", "-pk")
        verbose_name = _("interés en lista de espera")
        verbose_name_plural = _("intereses en lista de espera")

    def __str__(self):
        return f"{self.email} · {self.course or self.game}"

    def clean(self):
        super().clean()
        if self.course_id and self.game_id and self.course.game_id != self.game_id:
            raise ValidationError({"course": _("El curso debe ser del juego elegido.")})
        if self.legal_text_id and self.legal_text.kind != LegalText.Kind.PRIVACY:
            raise ValidationError({"legal_text": _("El aviso aceptado debe ser el de privacidad.")})


class LabStepProgress(models.Model):
    """Paso de la guía de laboratorio que un alumno marcó como hecho (EM-063)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lab_step_progress",
        verbose_name=_("alumno"),
    )
    step = models.ForeignKey(
        "catalog.LabStep",
        on_delete=models.CASCADE,
        related_name="progress",
        verbose_name=_("paso"),
    )
    completed_at = models.DateTimeField(_("fecha de completado"), default=timezone.now)

    class Meta:
        ordering = ("-completed_at", "-pk")
        verbose_name = _("paso de laboratorio completado")
        verbose_name_plural = _("pasos de laboratorio completados")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "step"), name="unique_lab_step_progress_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user} · {self.step}"
