from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseQuerySet(models.QuerySet):
    def published(self):
        """Cursos que pueden aparecer en páginas públicas."""
        return self.filter(status=Course.Status.PUBLISHED)


class Course(models.Model):
    """Práctica corta o curso por grupos de un juego. Precio y acceso son datos del admin."""

    class Kind(models.TextChoices):
        SHORT_PRACTICE = "short_practice", _("Práctica corta")
        COURSE = "course", _("Curso")

    class Level(models.TextChoices):
        BEGINNER = "beginner", _("Principiante")
        INTERMEDIATE = "intermediate", _("Intermedio")

    class Status(models.TextChoices):
        DRAFT = "draft", _("Borrador")
        PUBLISHED = "published", _("Publicado")

    title = models.CharField(_("título"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    # PROTECT: un juego con cursos se oculta, no se borra.
    game = models.ForeignKey(
        "catalog.Game",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("juego"),
    )
    kind = models.CharField(
        _("tipo"),
        max_length=20,
        choices=Kind,
        help_text=_(
            "Práctica corta: autoguiada, sin grupo, fechas ni cupo. Curso: se imparte por grupos."
        ),
    )
    level = models.CharField(_("nivel"), max_length=20, choices=Level)
    description = models.TextField(_("descripción"))
    requirements = models.TextField(_("requisitos"))
    duration_weeks = models.PositiveSmallIntegerField(
        _("duración en semanas"), validators=[MinValueValidator(1)]
    )
    price_cents = models.PositiveIntegerField(
        _("precio en centavos"),
        help_text=_("En MXN. Por ejemplo, 10000 son MXN 100.00."),
    )
    access_days = models.PositiveSmallIntegerField(
        _("días de acceso"),
        validators=[MinValueValidator(1)],
        help_text=_(
            "En una práctica corta se cuentan desde la inscripción; en un curso, "
            "desde que termina el grupo."
        ),
    )
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.DRAFT)

    objects = CourseQuerySet.as_manager()

    class Meta:
        ordering = ("title", "pk")
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")

    def __str__(self):
        return self.title
