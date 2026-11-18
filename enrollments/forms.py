from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from catalog.models import Game
from courses.models import Course


class WaitlistJoinForm(forms.Form):
    """Correo y juego o curso de interés, con el aviso de privacidad (EM-046)."""

    email = forms.EmailField(
        label=_("Correo"),
        error_messages={
            "invalid": _("Escribe un correo completo, por ejemplo nombre@dominio.mx."),
        },
    )
    game = forms.ModelChoiceField(
        queryset=Game.objects.none(),
        required=False,
        label=_("Juego de interés"),
        help_text=_("Elige el juego o, si ya hay un curso, el curso de abajo."),
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        required=False,
        label=_("Curso de interés"),
        help_text=_("Opcional. Si lo eliges, no hace falta repetir el juego."),
    )
    accept_privacy = forms.BooleanField(
        label=_("Acepto el aviso de privacidad."),
        error_messages={"required": _("Para dejar tu correo, acepta el aviso de privacidad.")},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo lo que ya es público: juegos activos y cursos publicados de esos juegos.
        self.fields["game"].queryset = Game.objects.filter(status=Game.Status.ACTIVE)
        self.fields["course"].queryset = (
            Course.objects.published()
            .filter(game__status=Game.Status.ACTIVE)
            .select_related("game")
            .order_by("game__name", "title")
        )
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["email"].help_text = _("Ahí te avisamos cuando abra el próximo grupo.")

    def clean_email(self):
        email = get_user_model().objects.normalize_email(self.cleaned_data["email"])
        return email.strip()

    def clean(self):
        cleaned = super().clean()
        game = cleaned.get("game")
        course = cleaned.get("course")
        if game is None and course is None:
            self.add_error("game", _("Elige un juego o un curso de interés."))
        elif course is not None and game is not None and course.game_id != game.pk:
            self.add_error("course", _("El curso que elegiste no es de ese juego."))
        elif course is not None and game is None:
            # El curso ya dice a qué juego pertenece; no se pide dos veces.
            cleaned["game"] = course.game
        return cleaned
