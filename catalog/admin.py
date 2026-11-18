from django import forms
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import Game, GameVersion, LabGuide, LabStep, ModdingEnvironment


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


class LabStepInline(admin.TabularInline):
    model = LabStep
    fields = ("order", "title", "instructions")
    extra = 0


@admin.register(LabGuide)
class LabGuideAdmin(admin.ModelAdmin):
    list_display = ("game", "game_version", "modding_environment", "steps_count")
    list_filter = ("game", "game_version", "modding_environment")
    search_fields = ("game__name", "game_version__number", "modding_environment__name")
    list_select_related = ("game", "game_version", "modding_environment")
    inlines = (LabStepInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(steps_count=Count("steps"))

    @admin.display(description=_("pasos"), ordering="steps_count")
    def steps_count(self, guide):
        return guide.steps_count


@admin.register(LabStep)
class LabStepAdmin(admin.ModelAdmin):
    list_display = ("title", "guide", "order")
    list_filter = ("guide__game",)
    search_fields = ("title", "guide__game__name")
    list_select_related = ("guide__game",)
