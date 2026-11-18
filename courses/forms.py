from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from catalog.models import GameVersion, ModdingEnvironment
from courses.models import LessonTest


class RevalidationForm(forms.ModelForm):
    """Registra una nueva prueba de la lección con su versión, entorno y fecha (EM-014)."""

    class Meta:
        model = LessonTest
        fields = ("game_version", "modding_environment", "tested_on")
        widgets = {"tested_on": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, game, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["game_version"].queryset = GameVersion.objects.filter(game=game).order_by(
            "-is_current", "-release_date", "number"
        )
        self.fields["modding_environment"].queryset = ModdingEnvironment.objects.filter(
            game=game
        ).order_by("name", "version")
        self.fields["game_version"].label_from_instance = lambda version: version.number
        self.fields["modding_environment"].label_from_instance = lambda environment: (
            f"{environment.name} {environment.version}"
        )
        self.fields["tested_on"].initial = timezone.localdate
        self.fields["tested_on"].label = _("Fecha en que se probó")
