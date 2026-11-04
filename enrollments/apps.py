from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EnrollmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "enrollments"
    verbose_name = _("Inscripciones")
