from django.db import models
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
