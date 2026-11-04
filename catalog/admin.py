from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Game, GameVersion, ModdingEnvironment


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "status", "official_url")
    list_filter = ("status",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    list_display = ("game", "number", "release_date", "is_current")
    list_filter = ("game", "is_current")
    search_fields = ("game__name", "number")
    list_select_related = ("game",)


class ModdingEnvironmentForm(forms.ModelForm):
    class Meta:
        model = ModdingEnvironment
        fields = ("game", "name", "version", "compatible_versions")

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get("game")
        versions = cleaned_data.get("compatible_versions")
        if game and versions is not None and versions.exclude(game=game).exists():
            self.add_error(
                "compatible_versions",
                _("Selecciona solo versiones del juego al que pertenece el entorno."),
            )
        return cleaned_data


@admin.register(ModdingEnvironment)
class ModdingEnvironmentAdmin(admin.ModelAdmin):
    form = ModdingEnvironmentForm
    list_display = ("name", "version", "game")
    list_filter = ("game",)
    search_fields = ("name", "version", "game__name")
    list_select_related = ("game",)
    filter_horizontal = ("compatible_versions",)
