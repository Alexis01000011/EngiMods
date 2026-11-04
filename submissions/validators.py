from urllib.parse import urlsplit

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_git_repository_url(value):
    """Acepta solo enlaces https a un repositorio (dueño/proyecto) en un servicio Git aceptado."""
    parts = urlsplit(value)
    host = (parts.hostname or "").lower().removeprefix("www.")
    hosts = [item.lower() for item in settings.GIT_REPOSITORY_HOSTS]
    segments = [segment for segment in parts.path.split("/") if segment]
    if parts.scheme != "https" or host not in hosts or len(segments) < 2:
        raise ValidationError(
            _(
                "Escribe el enlace https a tu repositorio en un servicio Git (%(hosts)s), "
                "por ejemplo https://github.com/usuario/mi-mod."
            ),
            code="invalid_git_repository_url",
            params={"hosts": ", ".join(hosts)},
        )
