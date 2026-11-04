from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Activo")
        HIDDEN = "hidden", _("Oculto")

    name = models.CharField(_("nombre"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=150, unique=True)
    description = models.TextField(_("descripción corta"))
    official_url = models.URLField(_("sitio oficial"))
    logo_url = models.URLField(_("URL del logo"), blank=True)
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.HIDDEN)

    class Meta:
        ordering = ("name", "pk")
        verbose_name = _("juego")
        verbose_name_plural = _("juegos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:game_detail", kwargs={"slug": self.slug})


class GameVersion(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="versions", verbose_name=_("juego")
    )
    number = models.CharField(_("número de versión"), max_length=100)
    release_date = models.DateField(_("fecha de publicación"))
    is_current = models.BooleanField(
        _("versión actual"),
        default=False,
        help_text=_("Desmarca la versión actual antes de marcar otra del mismo juego."),
    )

    class Meta:
        ordering = ("game__name", "-release_date", "number")
        verbose_name = _("versión del juego")
        verbose_name_plural = _("versiones del juego")
        constraints = [
            models.UniqueConstraint(
                fields=("game", "number"),
                name="catalog_game_version_unique",
            ),
            models.UniqueConstraint(
                fields=("game",),
                condition=models.Q(is_current=True),
                name="catalog_one_current_version_per_game",
                violation_error_message=_("Este juego ya tiene una versión actual."),
            ),
        ]

    def __str__(self):
        return f"{self.game} {self.number}"

    def clean(self):
        super().clean()
        if self.pk and self.game_id:
            if self.modding_environments.exclude(game_id=self.game_id).exists():
                raise ValidationError(
                    {"game": _("La versión tiene entornos compatibles de otro juego.")}
                )


class ModdingEnvironment(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="modding_environments",
        verbose_name=_("juego"),
    )
    name = models.CharField(_("nombre"), max_length=150)
    version = models.CharField(_("versión"), max_length=100)
    compatible_versions = models.ManyToManyField(
        GameVersion,
        blank=True,
        related_name="modding_environments",
        verbose_name=_("versiones del juego compatibles"),
    )

    class Meta:
        ordering = ("game__name", "name", "version")
        verbose_name = _("entorno de modding")
        verbose_name_plural = _("entornos de modding")
        constraints = [
            models.UniqueConstraint(
                fields=("game", "name", "version"),
                name="catalog_environment_version_unique",
            ),
        ]

    def __str__(self):
        return f"{self.game}: {self.name} {self.version}"

    def clean(self):
        super().clean()
        if self.pk and self.game_id:
            if self.compatible_versions.exclude(game_id=self.game_id).exists():
                raise ValidationError(
                    {"game": _("El entorno tiene versiones compatibles de otro juego.")}
                )


@receiver(m2m_changed, sender=ModdingEnvironment.compatible_versions.through)
def validate_compatibility(sender, instance, action, model, pk_set, **kwargs):
    """También protege las asociaciones hechas con add/set, en ambos sentidos."""
    if action == "pre_add" and pk_set:
        if model.objects.filter(pk__in=pk_set).exclude(game_id=instance.game_id).exists():
            raise ValidationError(
                _("El entorno y las versiones compatibles deben ser del mismo juego.")
            )
