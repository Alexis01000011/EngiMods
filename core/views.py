from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    """Página de inicio provisional. La landing real es la historia EM-040."""
    return render(request, "core/home.html")


def health(request):
    """Chequeo simple para el servidor de despliegue."""
    return JsonResponse({"status": "ok"})
