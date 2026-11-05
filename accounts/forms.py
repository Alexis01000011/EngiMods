from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    BaseUserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
    SetPasswordMixin,
)
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


class LoginForm(AuthenticationForm):
    """Inicio de sesión con correo y contraseña (EM-031)."""

    error_messages = {
        # No dice cuál de los dos falló: así no revela si el correo tiene cuenta.
        "invalid_login": _(
            "El correo o la contraseña no coinciden. Revísalos y vuelve a intentarlo; "
            "si olvidaste tu contraseña, puedes recuperarla."
        ),
        "inactive": _("Esta cuenta está desactivada."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Correo")
        self.fields["username"].widget = forms.EmailInput(
            attrs={"autofocus": True, "autocomplete": "email"}
        )
        self.fields["password"].label = _("Contraseña")


class PrivacyAcceptForm(forms.Form):
    """Aceptar la versión vigente del aviso de privacidad al iniciar sesión (EM-031)."""

    accept_privacy = forms.BooleanField(
        error_messages={"required": _("Para seguir, acepta el aviso de privacidad.")},
    )


class PasswordResetRequestForm(PasswordResetForm):
    """Pide el enlace para recuperar la contraseña (EM-031)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = _("Correo")
        self.fields["email"].help_text = _("El de tu cuenta. Ahí te enviamos el enlace.")
        self.fields["email"].error_messages["invalid"] = _(
            "Escribe un correo completo, por ejemplo nombre@dominio.mx."
        )


class NewPasswordForm(SetPasswordForm):
    """Contraseña nueva desde el enlace de recuperación (EM-031)."""

    new_password1, new_password2 = SetPasswordMixin.create_password_fields(
        label1=_("Contraseña nueva"), label2=_("Escribe otra vez tu contraseña nueva")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].help_text = _(
            "Usa una que no tengas en otro sitio. Si no es segura, te decimos qué cambiar."
        )
        self.fields["new_password2"].help_text = _("Así confirmamos que la escribiste bien.")
