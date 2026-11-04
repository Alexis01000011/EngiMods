from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class RegistrationForm(BaseUserCreationForm):
    """Registro público (EM-030): correo, nombre a mostrar, contraseña y aviso de privacidad."""

    password1, password2 = BaseUserCreationForm.create_password_fields(
        label1=_("Contraseña"), label2=_("Escribe otra vez tu contraseña")
    )
    accept_privacy = forms.BooleanField(
        error_messages={"required": _("Para crear tu cuenta, acepta el aviso de privacidad.")},
    )

    class Meta:
        model = User
        fields = ("email", "display_name")
        error_messages = {
            "email": {"invalid": _("Escribe un correo completo, por ejemplo nombre@dominio.mx.")},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["display_name"].widget.attrs["autocomplete"] = "nickname"
        self.fields["email"].help_text = _("Ahí te enviamos el enlace para verificar tu cuenta.")
        self.fields["password1"].help_text = _(
            "Usa una que no tengas en otro sitio. Si no es segura, te decimos qué cambiar."
        )
        self.fields["password2"].help_text = _("Así confirmamos que la escribiste bien.")

    def clean_email(self):
        email = User.objects.normalize_email(self.cleaned_data["email"])
        # Solo dice que el correo ya tiene cuenta; nada más de esa cuenta.
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                _(
                    "Ya hay una cuenta con este correo. Si es tuya, entra con ella; "
                    "si no, usa otro."
                ),
                code="duplicate_email",
            )
        return email
