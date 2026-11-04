from .models import LegalText


def legal_pages(request):
    """Indica qué páginas legales tienen versión vigente, para no enlazar a un 404."""
    return {"has_terms": LegalText.objects.current(LegalText.Kind.TERMS) is not None}
