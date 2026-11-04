from django import forms

from catalog.models import GameVersion, ModdingEnvironment

from .models import SubmissionAttempt


class SubmissionAttemptForm(forms.ModelForm):
    """Formulario del alumno. Solo ofrece versiones y entornos del juego del curso."""

    class Meta:
        model = SubmissionAttempt
        fields = ("repository_url", "game_version", "modding_environment", "comment")
        widgets = {"repository_url": forms.URLInput(attrs={"placeholder": "https://"})}

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
