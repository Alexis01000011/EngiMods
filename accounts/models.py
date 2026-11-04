from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from core.models import LegalText


class UserManager(BaseUserManager):
    """Manager para un usuario que inicia sesión con su correo en lugar de un username."""

    use_in_migrations = True

    def get_by_natural_key(self, email):
        # El correo no distingue mayúsculas: Ana@x.com y ana@x.com son la misma cuenta.
        return self.get(email__iexact=email)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("El correo es obligatorio."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Un superusuario debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Un superusuario debe tener is_superuser=True."))
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Usuario de EngiMods. El correo es el identificador para iniciar sesión."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_("correo electrónico"), unique=True)
    display_name = models.CharField(
        _("nombre a mostrar"),
        max_length=150,
        help_text=_("Así te verán tus tutores y compañeros."),
    )
    is_tutor = models.BooleanField(
        _("es tutor"),
        default=False,
        help_text=_("Puede acceder a las pantallas de tutoría sin entrar al administrador."),
    )
    email_verified_at = models.DateTimeField(
        _("correo verificado el"),
        null=True,
        blank=True,
        help_text=_(
            "Se llena cuando la persona abre el enlace del correo de registro. "
            "Sin correo verificado no puede pagar."
        ),
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["display_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="accounts_user_email_ci_unique",
                violation_error_message=_("Ya existe una cuenta con este correo."),
            ),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    @property
    def can_pay(self):
        """Sin correo verificado no se puede pagar (EM-030). EM-042 lo revisa antes del Checkout."""
        return self.is_active and self.email_verified_at is not None


class PrivacyConsent(models.Model):
    """Aceptación de una versión del aviso de privacidad.

    Quien acepta es un usuario (registro, EM-030) o, sin cuenta, un correo (lista de
    espera, EM-046). Nunca los dos.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuario"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="privacy_consents",
    )
    email = models.EmailField(
        _("correo"),
        blank=True,
        help_text=_("Solo cuando se acepta sin cuenta, por ejemplo en la lista de espera."),
    )
    # PROTECT: no se puede borrar una versión que alguien ya aceptó.
    legal_text = models.ForeignKey(
        LegalText,
        verbose_name=_("versión aceptada"),
        on_delete=models.PROTECT,
        limit_choices_to={"kind": LegalText.Kind.PRIVACY},
        related_name="privacy_consents",
    )
    accepted_at = models.DateTimeField(_("aceptado el"), auto_now_add=True)

    class Meta:
        verbose_name = _("consentimiento de privacidad")
        verbose_name_plural = _("consentimientos de privacidad")
        ordering = ["-accepted_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    (models.Q(user__isnull=False) & models.Q(email=""))
                    | (models.Q(user__isnull=True) & ~models.Q(email=""))
                ),
                name="accounts_privacyconsent_user_xor_email",
                violation_error_message=_(
                    "El consentimiento es de un usuario o de un correo, no de ambos."
                ),
            ),
        ]

    def __str__(self):
        return f"{self.user or self.email} · {self.legal_text}"
