#!/usr/bin/env python3
"""Exporta un documento Markdown a PDF con ReportLab.

Dependencias del sistema (sin instalar nada):

    /usr/bin/python3 -c "import reportlab, markdown"

Uso:

    /usr/bin/python3 docs/entrega-semestre/exportar_pdf.py \\
        docs/entrega-semestre/tecnico.md

Por omisión el PDF se escribe junto al Markdown, con el mismo nombre y
extensión ``.pdf``. El script no lee la red, no ejecuta comandos y no
modifica el archivo de entrada.

Soporta encabezados (h1 a h6), párrafos, listas ordenadas y desordenadas,
tablas, bloques de código, citas, separadores y formato inline (negritas,
cursivas, código y enlaces http/https/mailto o relativos). Los enlaces
relativos se conservan tal cual, sin convertirlos a rutas absolutas ni a
file://. Ante una construcción no soportada falla de forma explícita en
lugar de omitir contenido.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

DOCUMENT_DEPENDENCIES = ("markdown", "reportlab")


def _is_missing_document_dependency(exc: ImportError, roots: tuple[str, ...]) -> bool:
    if not isinstance(exc, ModuleNotFoundError) or not exc.name:
        return False
    return any(exc.name == root or exc.name.startswith(f"{root}.") for root in roots)


def _fail_missing_document_dependency(module_name: str) -> None:
    dependencies = ", ".join(DOCUMENT_DEPENDENCIES)
    print(
        f"error: falta el módulo externo '{module_name}'.\n"
        f"Dependencias documentales requeridas: {dependencies}.\n"
        "Usa un intérprete que ya las tenga; este script no instala paquetes.",
        file=sys.stderr,
    )
    raise SystemExit(1)


try:
    import markdown
except ImportError as exc:
    if _is_missing_document_dependency(exc, ("markdown",)):
        _fail_missing_document_dependency(exc.name or "markdown")
    raise

try:
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        HRFlowable,
        LongTable,
        PageTemplate,
        Paragraph,
        TableStyle,
    )
except ImportError as exc:
    if _is_missing_document_dependency(exc, ("reportlab",)):
        _fail_missing_document_dependency(exc.name or "reportlab")
    raise

# Carta y márgenes de una pulgada, como un documento de Word convencional.
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN_X = inch
MARGIN_TOP = inch
MARGIN_BOTTOM = inch
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)
CONTENT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

# Blanco, negro y grises; azul de hipervínculo sobrio.
TEXT = HexColor("#000000")
TEXT_SOFT = HexColor("#333333")
RULE = HexColor("#B7B7B7")
TABLE_RULE = HexColor("#A6A6A6")
CODE_BG = HexColor("#F2F2F2")
LINK_HEX = "#0563C1"
CODE_TEXT_HEX = "#000000"

BODY_SIZE = 11.0
CODE_SIZE = 9.2
CODE_PADDING = 5

INLINE_TAGS = {"strong", "b", "em", "i", "code", "a", "br"}
BLOCK_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "ul",
    "ol",
    "table",
    "pre",
    "blockquote",
    "hr",
}
ALLOWED_TAGS = INLINE_TAGS | BLOCK_TAGS | {"li", "thead", "tbody", "tr", "th", "td"}
SAFE_LINK_SCHEMES = {"http", "https", "mailto"}

FONT_SEARCH_DIRS = (
    Path("/usr/share/fonts/liberation"),
    Path("/usr/share/fonts/truetype/liberation"),
    Path("/usr/share/fonts/TTF"),
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/dejavu"),
    Path("/usr/local/share/fonts"),
)


class ExportError(Exception):
    """Error esperado durante la exportación."""


class Fonts:
    """Nombres de fuentes registradas en ReportLab."""

    def __init__(self) -> None:
        self.body = "Helvetica"
        self.body_bold = "Helvetica-Bold"
        self.mono = "Courier"
        self.warnings: list[str] = []


def _find_font(filename: str) -> Path | None:
    for directory in FONT_SEARCH_DIRS:
        candidate = directory / filename
        if candidate.is_file():
            return candidate
    return None


def _register_family(
    family: str,
    regular: str,
    bold: str,
    italic: str,
    bold_italic: str,
) -> tuple[str, str, str, str, str] | None:
    paths = [_find_font(name) for name in (regular, bold, italic, bold_italic)]
    if any(path is None for path in paths):
        return None

    names = [f"{family}-Regular", f"{family}-Bold", f"{family}-Italic", f"{family}-BoldItalic"]
    for name, path in zip(names, paths, strict=True):
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily(
        family,
        normal=names[0],
        bold=names[1],
        italic=names[2],
        boldItalic=names[3],
    )
    return family, names[0], names[1], names[2], names[3]


def load_fonts() -> Fonts:
    """Usa Liberation Sans si está disponible y avisa del fallback explícito."""
    fonts = Fonts()
    sans = _register_family(
        "EngiSans",
        "LiberationSans-Regular.ttf",
        "LiberationSans-Bold.ttf",
        "LiberationSans-Italic.ttf",
        "LiberationSans-BoldItalic.ttf",
    )
    if sans is None:
        fonts.warnings.append(
            "no se encontró Liberation Sans completa; se usa Helvetica para el texto"
        )
    else:
        fonts.body, fonts.body_bold = sans[1], sans[2]

    mono = _register_family(
        "EngiMono",
        "LiberationMono-Regular.ttf",
        "LiberationMono-Bold.ttf",
        "LiberationMono-Italic.ttf",
        "LiberationMono-BoldItalic.ttf",
    )
    if mono is None:
        mono = _register_family(
            "EngiMono",
            "DejaVuSansMono.ttf",
            "DejaVuSansMono-Bold.ttf",
            "DejaVuSansMono-Oblique.ttf",
            "DejaVuSansMono-BoldOblique.ttf",
        )
        if mono is None:
            fonts.warnings.append(
                "no se encontró Liberation Mono ni DejaVu Sans Mono; se usa Courier para el código"
            )
        else:
            fonts.warnings.append(
                "no se encontró Liberation Mono; se usa DejaVu Sans Mono para el código"
            )
    if mono is not None:
        fonts.mono = mono[1]

    return fonts


def _escape_text(text: str) -> str:
    text = text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return html.escape(text, quote=False)


def _normalize_text(text: str) -> str:
    return " ".join(text.split())


def _format_size(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _validate_link(href: str) -> None:
    """Acepta enlaces web, correo y rutas relativas sin convertirlas a file://."""
    if not href:
        raise ExportError("hay un enlace sin destino (href vacío)")
    if href.startswith("#"):
        raise ExportError(f"ancla interna no soportada en PDF: {href!r}")
    if href.startswith(("/", "~")) and not href.startswith("//"):
        raise ExportError(f"no se permiten rutas locales absolutas en enlaces: {href!r}")

    parsed = urlparse(href)
    scheme = parsed.scheme.lower()
    if scheme:
        if scheme not in SAFE_LINK_SCHEMES:
            raise ExportError(
                f"enlace no soportado (solo http, https, mailto o rutas relativas): {href!r}"
            )
    elif not parsed.path and not parsed.netloc:
        raise ExportError(f"enlace relativo sin ruta utilizable: {href!r}")


def _validate_tree(node: ET.Element) -> None:
    for child in node:
        tag = child.tag
        if not isinstance(tag, str):
            raise ExportError("el Markdown contiene un comentario o instrucción XML no soportada")
        if tag == "img":
            raise ExportError(
                "las imágenes no están soportadas por este exportador; "
                "quita la imagen o conviértela a una tabla o texto"
            )
        if tag not in ALLOWED_TAGS:
            raise ExportError(f"etiqueta HTML no soportada en el Markdown: <{tag}>")
        if tag == "a":
            _validate_link((child.get("href") or "").strip())
        _validate_tree(child)


def _parse_markdown(source_text: str) -> ET.Element:
    try:
        rendered = markdown.markdown(
            source_text,
            extensions=["tables", "fenced_code", "sane_lists"],
            output_format="xhtml",
        )
    except Exception as exc:  # markdown no documenta un tipo de error único
        raise ExportError(f"Markdown inválido: {exc}") from exc

    try:
        root = ET.fromstring(f"<root>{rendered}</root>")
    except ET.ParseError as exc:
        raise ExportError(
            "el HTML generado por Markdown no es XML válido; "
            f"revisa el HTML incrustado en el documento ({exc})"
        ) from exc

    _validate_tree(root)
    return root


def _first_heading_text(root: ET.Element) -> str:
    for element in root.iter("h1"):
        title = _normalize_text("".join(element.itertext()))
        if title:
            return title
    return ""


def _alignment_from_style(style: str | None):
    match = re.search(r"text-align\s*:\s*(left|right|center|justify)", style or "")
    if match is None:
        return TA_LEFT
    return {
        "left": TA_LEFT,
        "right": TA_RIGHT,
        "center": TA_CENTER,
        "justify": TA_JUSTIFY,
    }[match.group(1)]


class PdfExporter:
    """Convierte el árbol HTML de Markdown en flowables de ReportLab."""

    def __init__(self, fonts: Fonts) -> None:
        self.fonts = fonts
        self.styles = self._build_styles()
        self._style_cache: dict[tuple, ParagraphStyle] = {}

    def _build_styles(self) -> dict[str, ParagraphStyle]:
        fonts = self.fonts
        styles: dict[str, ParagraphStyle] = {}

        styles["body"] = ParagraphStyle(
            "Body",
            fontName=fonts.body,
            fontSize=BODY_SIZE,
            leading=12.8,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=6,
            allowWidows=0,
            allowOrphans=0,
        )
        heading_sizes = {
            1: (15.5, 19, 0, 8),
            2: (13, 16, 12, 4),
            3: (11.5, 14, 10, 3),
            4: (11, 13.5, 8, 2),
            5: (11, 13.5, 6, 2),
            6: (11, 13.5, 6, 2),
        }
        for level, (size, leading, before, after) in heading_sizes.items():
            styles[f"h{level}"] = ParagraphStyle(
                f"Heading{level}",
                fontName=fonts.body_bold,
                fontSize=size,
                leading=leading,
                textColor=TEXT,
                alignment=TA_LEFT,
                spaceBefore=before,
                spaceAfter=after,
            )

        styles["code"] = ParagraphStyle(
            "Code",
            fontName=fonts.mono,
            fontSize=CODE_SIZE,
            leading=11.2,
            textColor=TEXT,
            backColor=CODE_BG,
            borderPadding=CODE_PADDING,
            spaceBefore=3,
            spaceAfter=6,
        )
        styles["cell"] = ParagraphStyle(
            "TableCell",
            fontName=fonts.body,
            fontSize=9.5,
            leading=11.5,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=0,
        )
        styles["cell_head"] = ParagraphStyle(
            "TableHead",
            parent=styles["cell"],
            fontName=fonts.body_bold,
        )
        return styles

    def _body_style(self, indent: float = 0, quote: bool = False) -> ParagraphStyle:
        if indent == 0 and not quote:
            return self.styles["body"]
        key = ("body", indent, quote)
        if key not in self._style_cache:
            self._style_cache[key] = ParagraphStyle(
                f"Body-{indent}-{quote}",
                parent=self.styles["body"],
                leftIndent=indent,
                textColor=TEXT_SOFT if quote else TEXT,
            )
        return self._style_cache[key]

    def _list_style(
        self,
        indent: float,
        bullet_font: str,
        quote: bool,
    ) -> ParagraphStyle:
        key = ("list", indent, bullet_font, quote)
        if key not in self._style_cache:
            self._style_cache[key] = ParagraphStyle(
                f"List-{indent}-{bullet_font}-{quote}",
                parent=self.styles["body"],
                leftIndent=indent,
                bulletIndent=max(0, indent - 14),
                bulletFontName=bullet_font,
                bulletFontSize=BODY_SIZE,
                textColor=TEXT_SOFT if quote else TEXT,
                spaceAfter=2,
            )
        return self._style_cache[key]

    def _continuation_style(self, indent: float, quote: bool) -> ParagraphStyle:
        key = ("continuation", indent, quote)
        if key not in self._style_cache:
            self._style_cache[key] = ParagraphStyle(
                f"Continue-{indent}-{quote}",
                parent=self._body_style(indent, quote),
                spaceAfter=2,
            )
        return self._style_cache[key]

    def _cell_style(self, header: bool, align: int) -> ParagraphStyle:
        key = ("cell", header, align)
        if key not in self._style_cache:
            parent = self.styles["cell_head"] if header else self.styles["cell"]
            self._style_cache[key] = ParagraphStyle(
                f"Cell-{header}-{align}",
                parent=parent,
                alignment=align,
            )
        return self._style_cache[key]

    def _inline_element(self, element: ET.Element, style: ParagraphStyle) -> str:
        tag = element.tag
        if tag == "br":
            return "<br/>"
        if tag in {"strong", "b"}:
            return f"<b>{self._inline_text(element, style)}</b>"
        if tag in {"em", "i"}:
            return f"<i>{self._inline_text(element, style)}</i>"
        if tag == "code":
            code_text = _normalize_text("".join(element.itertext()))
            size = _format_size(max(6.8, style.fontSize - 0.8))
            return (
                f'<font name="{self.fonts.mono}" size="{size}" '
                f'color="{CODE_TEXT_HEX}">{html.escape(code_text, quote=False)}</font>'
            )
        if tag == "a":
            href = (element.get("href") or "").strip()
            _validate_link(href)
            inner = self._inline_text(element, style)
            if not inner:
                inner = html.escape(href, quote=False)
            return (
                f'<a href="{html.escape(href, quote=True)}" color="{LINK_HEX}"><u>{inner}</u></a>'
            )
        if tag == "img":
            raise ExportError("las imágenes no están soportadas por este exportador")
        raise ExportError(f"formato inline no soportado: <{tag}>")

    def _inline_text(self, element: ET.Element, style: ParagraphStyle) -> str:
        parts: list[str] = []
        if element.text:
            parts.append(_escape_text(element.text))
        for child in element:
            parts.append(self._inline_element(child, style))
            if child.tail:
                parts.append(_escape_text(child.tail))
        return "".join(parts)

    def _cell_markup(self, cell: ET.Element, style: ParagraphStyle) -> str:
        parts: list[str] = []
        if cell.text:
            parts.append(_escape_text(cell.text))
        for child in cell:
            if child.tag == "p":
                parts.append(self._inline_text(child, style))
            elif child.tag in INLINE_TAGS:
                parts.append(self._inline_element(child, style))
            else:
                raise ExportError(
                    f"contenido no soportado dentro de una celda de tabla: <{child.tag}>"
                )
            if child.tail:
                parts.append(_escape_text(child.tail))
        return "<br/>".join(part for part in parts if part.strip())

    def _render_heading(self, element: ET.Element, story: list) -> None:
        level = int(element.tag[1])
        style = self.styles[f"h{level}"]
        markup = self._inline_text(element, style)
        if markup.strip():
            story.append(Paragraph(markup, style))

    def _render_paragraph(
        self,
        element: ET.Element,
        story: list,
        indent: float = 0,
        quote: bool = False,
    ) -> None:
        style = self._body_style(indent, quote)
        markup = self._inline_text(element, style)
        if markup.strip():
            story.append(Paragraph(markup, style))

    def _render_blockquote(
        self,
        element: ET.Element,
        story: list,
        indent: float = 0,
    ) -> None:
        if element.text and element.text.strip():
            raise ExportError("texto suelto no soportado dentro de una cita")
        for child in element:
            self._render_block(child, story, indent + 16, True)
            if child.tail and child.tail.strip():
                raise ExportError("texto suelto no soportado dentro de una cita")

    def _render_code(self, element: ET.Element, story: list, indent: float = 0) -> None:
        code_text = "".join(element.itertext())
        code_text = code_text.replace("\r\n", "\n").replace("\r", "\n").expandtabs(4)
        if code_text.startswith("\n"):
            code_text = code_text[1:]
        if code_text.endswith("\n"):
            code_text = code_text[:-1]

        if not code_text:
            return

        char_width = pdfmetrics.stringWidth("0123456789", self.fonts.mono, CODE_SIZE) / 10
        usable_width = CONTENT_WIDTH - indent - (2 * CODE_PADDING) - 6
        max_chars = max(20, int(usable_width / char_width))

        lines: list[str] = []
        for raw_line in code_text.split("\n"):
            if not raw_line:
                lines.append("")
                continue
            while len(raw_line) > max_chars:
                lines.append(raw_line[:max_chars])
                raw_line = raw_line[max_chars:]
            lines.append(raw_line)

        escaped = [html.escape(line, quote=False).replace(" ", "\u00a0") for line in lines]
        markup = "<br/>".join(escaped)
        style = ParagraphStyle(
            f"Code-{indent}",
            parent=self.styles["code"],
            leftIndent=indent,
        )
        story.append(Paragraph(markup, style))

    def _render_table(self, element: ET.Element, story: list, indent: float = 0) -> None:
        all_rows = [row for row in element.iter("tr")]
        if not all_rows:
            raise ExportError("tabla sin filas")

        parents = {child: parent for parent in element.iter() for child in list(parent)}
        header_rows: list[ET.Element] = []
        body_rows: list[ET.Element] = []
        for row in all_rows:
            parent = parents.get(row)
            if parent is not None and parent.tag == "thead":
                header_rows.append(row)
            else:
                body_rows.append(row)
        rows = header_rows + body_rows

        table_data: list[list[Paragraph]] = []
        plain_cells: list[list[str]] = []
        column_count = 0
        for row_index, row in enumerate(rows):
            cells = [cell for cell in row if cell.tag in {"th", "td"}]
            if not cells:
                raise ExportError("fila de tabla sin celdas")
            if column_count and len(cells) != column_count:
                raise ExportError(
                    "fila de tabla con un número distinto de columnas; "
                    "revisa la sintaxis de la tabla"
                )
            column_count = len(cells)
            header = row_index < len(header_rows)
            rendered_row: list[Paragraph] = []
            plain_row: list[str] = []
            for cell in cells:
                align = _alignment_from_style(cell.get("style"))
                style = self._cell_style(header, align)
                rendered_row.append(Paragraph(self._cell_markup(cell, style), style))
                plain_row.append(_normalize_text("".join(cell.itertext())))
            table_data.append(rendered_row)
            plain_cells.append(plain_row)

        if column_count == 0:
            raise ExportError("tabla sin columnas")

        available = CONTENT_WIDTH - indent - 2
        min_column = 26.0
        if column_count * min_column > available:
            raise ExportError(
                "la tabla tiene demasiadas columnas para el ancho de la página; "
                "divídela en tablas más pequeñas"
            )

        weights = [
            max(1.0, min(60.0, max(len(row[index]) for row in plain_cells))) ** 0.8
            for index in range(column_count)
        ]
        weight_total = sum(weights)
        extra = available - (column_count * min_column)
        widths = [min_column + (extra * weight / weight_total) for weight in weights]

        table = LongTable(
            table_data,
            colWidths=widths,
            repeatRows=len(header_rows),
            hAlign="LEFT",
            splitByRow=1,
        )
        commands = [
            ("GRID", (0, 0), (-1, -1), 0.5, TABLE_RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ]
        if len(body_rows) >= 2:
            last_row = len(header_rows) + len(body_rows) - 1
            commands.append(("NOSPLIT", (0, last_row - 1), (-1, last_row)))
        table.setStyle(TableStyle(commands))
        table.spaceBefore = 4
        table.spaceAfter = 6
        story.append(table)

    def _flush_list_text(
        self,
        parts: list[str],
        story: list,
        first_style: ParagraphStyle,
        continuation_style: ParagraphStyle,
        marker: str | None,
        used: bool,
    ) -> bool:
        markup = "".join(parts).strip()
        parts.clear()
        if not markup:
            return used
        if not used:
            story.append(Paragraph(markup, first_style, bulletText=marker or ""))
            return True
        story.append(Paragraph(markup, continuation_style))
        return True

    def _render_list_item(
        self,
        item: ET.Element,
        story: list,
        marker: str,
        depth: int,
        indent: float,
        quote: bool,
    ) -> None:
        left = indent + 18 + (depth * 16)
        first_style = self._list_style(left, self.fonts.body, quote)
        continuation_style = self._continuation_style(left, quote)
        parts: list[str] = []
        used = False
        has_block = False

        if item.text:
            parts.append(_escape_text(item.text))

        for child in item:
            if child.tag in INLINE_TAGS:
                parts.append(self._inline_element(child, self.styles["body"]))
            elif child.tag == "p":
                used = self._flush_list_text(
                    parts, story, first_style, continuation_style, marker, used
                )
                content = self._inline_text(child, self.styles["body"])
                if content.strip():
                    if not used:
                        story.append(Paragraph(content, first_style, bulletText=marker))
                        used = True
                    else:
                        story.append(Paragraph(content, continuation_style))
            elif child.tag in {"ul", "ol"}:
                used = self._flush_list_text(
                    parts, story, first_style, continuation_style, marker, used
                )
                self._render_list(child, story, depth + 1, indent, quote)
                has_block = True
            elif child.tag in {"pre", "table", "blockquote", "hr"}:
                used = self._flush_list_text(
                    parts, story, first_style, continuation_style, marker, used
                )
                self._render_block(child, story, left, quote)
                has_block = True
            else:
                raise ExportError(
                    f"contenido no soportado dentro de un elemento de lista: <{child.tag}>"
                )
            if child.tail:
                parts.append(_escape_text(child.tail))

        used = self._flush_list_text(parts, story, first_style, continuation_style, marker, used)
        if not used and not has_block:
            story.append(Paragraph("", first_style, bulletText=marker))

    def _render_list(
        self,
        element: ET.Element,
        story: list,
        depth: int = 0,
        indent: float = 0,
        quote: bool = False,
    ) -> None:
        ordered = element.tag == "ol"
        items = [child for child in element if child.tag == "li"]
        if not items:
            raise ExportError("lista sin elementos")
        if element.text and element.text.strip():
            raise ExportError("texto suelto no soportado dentro de una lista")

        start = 1
        if ordered:
            raw_start = (element.get("start") or "1").strip()
            try:
                start = int(raw_start)
            except ValueError as exc:
                raise ExportError(f"lista ordenada con inicio inválido: {raw_start!r}") from exc

        for index, item in enumerate(items):
            marker = f"{start + index}." if ordered else "\u2022"
            self._render_list_item(item, story, marker, depth, indent, quote)

    def _render_block(
        self,
        element: ET.Element,
        story: list,
        indent: float = 0,
        quote: bool = False,
    ) -> None:
        tag = element.tag
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._render_heading(element, story)
        elif tag == "p":
            self._render_paragraph(element, story, indent, quote)
        elif tag in {"ul", "ol"}:
            self._render_list(element, story, 0, indent, quote)
        elif tag == "table":
            self._render_table(element, story, indent)
        elif tag == "pre":
            self._render_code(element, story, indent)
        elif tag == "blockquote":
            self._render_blockquote(element, story, indent)
        elif tag == "hr":
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=RULE,
                    spaceBefore=2,
                    spaceAfter=6,
                )
            )
        else:
            raise ExportError(f"bloque Markdown no soportado: <{tag}>")

    def build_story(self, root: ET.Element) -> list:
        self._reject_stray_text(root)
        story: list = []
        if root.text and root.text.strip():
            raise ExportError("texto suelto no soportado fuera de un bloque Markdown")
        for element in root:
            self._render_block(element, story)
            if element.tail and element.tail.strip():
                raise ExportError("texto suelto no soportado fuera de un bloque Markdown")
        self._keep_headings_with_paragraphs(story)
        return story

    @staticmethod
    def _keep_headings_with_paragraphs(story: list) -> None:
        for index, flowable in enumerate(story[:-1]):
            if not isinstance(flowable, Paragraph):
                continue
            if not flowable.style.name.startswith("Heading"):
                continue
            next_flowable = story[index + 1]
            if not isinstance(next_flowable, Paragraph):
                continue
            if next_flowable.style.name.startswith(("Heading", "Code")):
                continue
            flowable.keepWithNext = 1

    def _reject_stray_text(self, root: ET.Element) -> None:
        """Evita que texto fuera de párrafos, celdas o elementos de lista se pierda."""
        structural = {"table", "thead", "tbody", "tr", "ul", "ol"}
        for node in root.iter():
            if node.tag not in structural:
                continue
            if node.text and node.text.strip():
                raise ExportError(f"texto suelto no soportado dentro de <{node.tag}>")
            for child in node:
                if child.tail and child.tail.strip():
                    raise ExportError(f"texto suelto no soportado dentro de <{node.tag}>")


def _resolve_paths(input_arg: Path, output_arg: Path | None, force: bool) -> tuple[Path, Path]:
    source = input_arg.expanduser().resolve()
    if not source.is_file():
        raise ExportError(f"no existe el archivo de entrada: {source}")
    if source.suffix.lower() not in {".md", ".markdown"}:
        raise ExportError("la entrada debe ser un archivo Markdown (.md o .markdown)")

    default_output = source.with_suffix(".pdf")
    output_candidate = output_arg.expanduser() if output_arg else default_output
    if output_candidate.suffix.lower() != ".pdf":
        raise ExportError("la salida debe tener extensión .pdf")
    if output_candidate.is_symlink():
        raise ExportError(f"no se escribe sobre un enlace simbólico: {output_candidate}")
    output = output_candidate.resolve()
    if output == source:
        raise ExportError("la salida no puede ser el archivo de entrada")
    if output.exists() and not output.is_file():
        raise ExportError(f"la salida no es un archivo regular: {output}")
    if not output.parent.is_dir():
        raise ExportError(f"no existe el directorio de salida: {output.parent}")

    is_default = output == default_output
    if output.exists() and not is_default and not force:
        raise ExportError(f"la salida ya existe: {output}. Usa --force para reemplazarla.")
    return source, output


def export_markdown(source: Path, output: Path) -> None:
    try:
        source_text = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ExportError(f"el archivo no es UTF-8 válido: {source}") from exc
    except OSError as exc:
        raise ExportError(f"no se pudo leer la entrada: {exc}") from exc

    root = _parse_markdown(source_text)
    title = _first_heading_text(root) or source.stem
    fonts = load_fonts()
    for warning in fonts.warnings:
        print(f"aviso: {warning}", file=sys.stderr)

    temp_path: Path | None = None
    try:
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{output.stem}-",
            suffix=".tmp.pdf",
            dir=str(output.parent),
        )
        os.close(fd)
        temp_path = Path(temp_name)

        frame = Frame(
            MARGIN_X,
            MARGIN_BOTTOM,
            CONTENT_WIDTH,
            CONTENT_HEIGHT,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="body",
        )
        document = BaseDocTemplate(
            str(temp_path),
            pagesize=letter,
            leftMargin=MARGIN_X,
            rightMargin=MARGIN_X,
            topMargin=MARGIN_TOP,
            bottomMargin=MARGIN_BOTTOM,
            pageTemplates=[PageTemplate(id="Body", frames=[frame])],
            title=title,
            author="EngiMods",
            subject="Documentación técnica de EngiMods",
            creator="exportar_pdf.py",
        )
        exporter = PdfExporter(fonts)
        story = exporter.build_story(root)
        if not story:
            raise ExportError("el Markdown no contiene contenido exportable")

        document.build(story)
        os.replace(temp_path, output)
        temp_path = None
    except OSError as exc:
        raise ExportError(f"no se pudo escribir el PDF: {exc}") from exc
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Exporta un Markdown a PDF con ReportLab.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplo:\n"
            "  /usr/bin/python3 docs/entrega-semestre/exportar_pdf.py \\\n"
            "      docs/entrega-semestre/tecnico.md\n\n"
            "El PDF se escribe junto al Markdown salvo que se indique -o."
        ),
    )
    parser.add_argument("entrada", type=Path, help="archivo Markdown de entrada")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="PDF de salida (por omisión: hermano del Markdown con extensión .pdf)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="permite reemplazar un PDF existente indicado explícitamente",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        source, output = _resolve_paths(args.entrada, args.output, args.force)
        export_markdown(source, output)
    except ExportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"PDF generado: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
