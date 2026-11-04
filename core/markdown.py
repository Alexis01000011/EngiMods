"""Markdown a HTML seguro para el contenido que se captura en el admin."""

import markdown
import nh3
from django.utils.safestring import mark_safe

EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


def render_markdown(text):
    """Convierte Markdown a HTML y lo sanitiza: sin scripts, eventos ni enlaces javascript:."""
    html = markdown.markdown(text, extensions=EXTENSIONS)
    return mark_safe(nh3.clean(html))
