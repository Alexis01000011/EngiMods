from django import forms
from django.utils.translation import gettext_lazy as _

from .models import LiveSession


class LiveSessionForm(forms.ModelForm):
    """El tutor registra una clínica en uno de sus grupos (EM-052)."""

    class Meta:
        model = LiveSession
        fields = ("cohort", "date", "start_time", "topic", "join_url")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "join_url": forms.URLInput(attrs={"placeholder": "https://"}),
        }

    def __init__(self, *args, cohorts, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cohort"].queryset = cohorts
        self.fields["cohort"].label_from_instance = lambda cohort: (
            f"{cohort.course.title} · {cohort.name}"
        )
        self.fields["start_time"].help_text = _("Hora de Ciudad de México.")
