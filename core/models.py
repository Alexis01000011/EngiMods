from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class LegalTextQuerySet(models.QuerySet):
    def current(self, kind):
        """Versión vigente: la de fecha de vigencia más reciente que ya llegó, o None."""
        return (
            self.filter(kind=kind, effective_date__lte=timezone.localdate())
            .order_by("-effective_date", "-pk")
            .first()
        )


class LegalText(models.Model):
    """Texto legal versionado. Se captura en el admin; las plantillas solo lo muestran."""

    class Kind(models.TextChoices):
        PRIVACY = "privacy", _("Aviso de privacidad")

    kind = models.CharField(_("tipo"), max_length=20, choices=Kind.choices)
    version = models.CharField(_("versión"), max_length=20, help_text=_("Por ejemplo, 1.0."))
    body = models.TextField(
        _("texto"),
        help_text=_("Texto plano. Una línea en blanco separa párrafos."),
    )
    effective_date = models.DateField(
        _("vigente desde"),
        help_text=_(
            "Se muestra la versión con la fecha más reciente que ya llegó. "
            "Puedes capturar una versión nueva antes de que entre en vigor."
        ),
    )

    objects = LegalTextQuerySet.as_manager()

    class Meta:
        verbose_name = _("texto legal")
        verbose_name_plural = _("textos legales")
        ordering = ["kind", "-effective_date", "-pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["kind", "version"],
                name="core_legaltext_kind_version_unique",
                violation_error_message=_("Ya existe esa versión para este tipo de texto."),
            ),
        ]

    def __str__(self):
        return f"{self.get_kind_display()} {self.version}"
