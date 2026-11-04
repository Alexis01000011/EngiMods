import pytest
from django.utils.safestring import SafeString

from core.markdown import render_markdown


def test_convierte_markdown_con_codigo_y_tablas():
    html = render_markdown(
        "# Título\n\nTexto con **negritas**.\n\n```python\nprint('hola')\n```\n\n"
        "| a | b |\n|---|---|\n| 1 | 2 |"
    )
    assert isinstance(html, SafeString)
    assert "<h1>Título</h1>" in html
    assert "<strong>negritas</strong>" in html
    assert "<pre><code>" in html
    assert "<td>1</td>" in html


@pytest.mark.parametrize(
    ("source", "forbidden"),
    [
        ("<script>alert(1)</script>", "alert(1)"),
        ("[clic](javascript:alert(1))", "javascript:"),
        ('<img src="x.png" onerror="alert(1)">', "onerror"),
        ('<a href="https://example.com/" onclick="alert(1)">x</a>', "onclick"),
        ('<iframe src="https://example.com/"></iframe>', "<iframe"),
    ],
)
def test_quita_scripts_y_html_inseguro(source, forbidden):
    assert forbidden not in render_markdown(source)


def test_conserva_enlaces_seguros():
    html = render_markdown("[Sitio](https://example.com/)")
    assert 'href="https://example.com/"' in html
