"""Protección común de las pantallas de tutoría, independiente del admin."""

from functools import wraps

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


def has_tutor_access(user):
    return user.is_authenticated and user.is_active and (user.is_tutor or user.is_superuser)


def tutor_required(view):
    """Responde 403 si la cuenta no es un tutor activo o un superusuario activo."""

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not has_tutor_access(request.user):
            raise PermissionDenied(_("No tienes permiso para entrar a las pantallas de tutoría."))
        return view(request, *args, **kwargs)

    return wrapped


class TutorRequiredMixin(AccessMixin):
    """Colocar antes de View en las vistas de tutoría basadas en clases."""

    raise_exception = True
    permission_denied_message = _("No tienes permiso para entrar a las pantallas de tutoría.")

    def dispatch(self, request, *args, **kwargs):
        if not has_tutor_access(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
