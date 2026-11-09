from django import forms
from django.utils.translation import gettext_lazy as _

from catalog.models import GameVersion, ModdingEnvironment

from .models import Review, ReviewScore, SubmissionAttempt


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


class ReviewForm(forms.Form):
    """Formulario del tutor: un nivel por criterio de la rúbrica, comentario general y decisión."""

    comment = forms.CharField(
        label=_("Comentario general"),
        widget=forms.Textarea,
        help_text=_("Qué hizo bien y qué puede mejorar. El alumno lo lee junto con la rúbrica."),
        error_messages={"required": _("Escribe un comentario para el alumno.")},
    )
    decision = forms.ChoiceField(
        label=_("Decisión"),
        choices=Review.Decision.choices,
        widget=forms.RadioSelect,
        error_messages={"required": _("Elige si la apruebas o si pides cambios.")},
    )

    def __init__(self, *args, criteria, **kwargs):
        super().__init__(*args, **kwargs)
        self.criteria = list(criteria)
        for criterion in self.criteria:
            self.fields[self.criterion_field(criterion)] = forms.ChoiceField(
                label=criterion.title,
                help_text=criterion.description,
                choices=ReviewScore.Level.choices,
                widget=forms.RadioSelect,
                error_messages={"required": _("Elige un nivel para este criterio.")},
            )
        self.order_fields([self.criterion_field(c) for c in self.criteria] + ["comment"])

    @staticmethod
    def criterion_field(criterion):
        return f"criterion_{criterion.pk}"

    def scores(self):
        """Pares (criterio, nivel) ya validados."""
        return [(c, self.cleaned_data[self.criterion_field(c)]) for c in self.criteria]
