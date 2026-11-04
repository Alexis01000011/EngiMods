from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _


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
