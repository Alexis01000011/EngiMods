from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from .models import LegalText


def home(request):
    """Página de inicio provisional. La landing real es la historia EM-040."""
    return render(request, "core/home.html")


def health(request):
    """Chequeo simple para el servidor de despliegue."""
    return JsonResponse({"status": "ok"})


def privacy(request):
    """Aviso de privacidad vigente. El texto se captura en el admin (LegalText)."""
    legal_text = LegalText.objects.current(LegalText.Kind.PRIVACY)
    if legal_text is None:
        raise Http404(_("Todavía no hay un aviso de privacidad vigente."))
    return render(request, "core/legal_text.html", {"legal_text": legal_text})
