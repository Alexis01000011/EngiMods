"""Clínicas en vivo de los grupos del tutor (EM-052)."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from accounts.permissions import tutor_required

from .forms import LiveSessionForm
from .models import Cohort


def tutor_cohorts(user):
    """Los grupos del tutor; un superusuario ve todos."""
    cohorts = Cohort.objects.select_related("course").prefetch_related("live_sessions")
    if user.is_superuser:
        return cohorts
    return cohorts.filter(tutors=user)


@tutor_required
def sessions(request):
    cohorts = tutor_cohorts(request.user)
    form = LiveSessionForm(request.POST or None, cohorts=cohorts)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Listo. La clínica ya aparece en el panel de tus alumnos."))
        return redirect("clinics:sessions")
    return render(
        request,
        "cohorts/live_sessions.html",
        {"cohorts": cohorts, "form": form},
    )
