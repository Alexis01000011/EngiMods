"""El bloque @theme de assets/tailwind.css tiene los mismos valores que DESIGN.md (ADR 0002)."""

import re

from django.conf import settings

DESIGN = settings.BASE_DIR / "DESIGN.md"
THEME = settings.BASE_DIR / "assets" / "tailwind.css"

# Grupo de DESIGN.md y prefijo de su variable en el tema de Tailwind.
PREFIXES = {"colors": "color", "rounded": "radius", "spacing": "spacing"}
# Propiedad de un token de typography y sufijo de su variable --text-<nombre>.
TEXT_SUFFIXES = {
    "fontSize": "",
    "fontWeight": "--font-weight",
    "lineHeight": "--line-height",
    "letterSpacing": "--letter-spacing",
}
FAMILIES = {"source serif 4": "serif", "plus jakarta sans": "sans", "jetbrains mono": "mono"}


def normalize(value):
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.replace("'", '"').lower()


def design_tokens():
    front = DESIGN.read_text(encoding="utf-8").split("---", 2)[1]
    tokens, group, name = {}, None, None
    for line in front.splitlines():
        if top := re.match(r"^([a-z]+):\s*$", line):
            group = top.group(1)
        elif re.match(r"^\S", line):
            group = None
        elif group in PREFIXES and (item := re.match(r"^  ([a-z0-9-]+):\s*(.+)$", line)):
            tokens[f"--{PREFIXES[group]}-{item.group(1)}"] = normalize(item.group(2))
        elif group == "typography" and (item := re.match(r"^  ([a-z0-9-]+):\s*$", line)):
            name = item.group(1)
        elif group == "typography" and (prop := re.match(r"^    (\w+):\s*(.+)$", line)):
            key, value = prop.group(1), normalize(prop.group(2))
            if key == "fontFamily":
                family = value.split(",")[0].strip('"')
                tokens[f"--font-{FAMILIES[family]}"] = value
            else:
                tokens[f"--text-{name}{TEXT_SUFFIXES[key]}"] = value
    return tokens


def theme_tokens():
    block = re.search(r"@theme \{(.*?)\n\}", THEME.read_text(encoding="utf-8"), re.S).group(1)
    pairs = re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", block)
    return {name: normalize(value) for name, value in pairs}


def test_el_tema_tiene_cada_valor_de_design_md():
    design, theme = design_tokens(), theme_tokens()
    # Se leyeron los cinco grupos de DESIGN.md.
    for name in ("--color-ink", "--radius-lg", "--spacing-md", "--text-title-lg", "--font-serif"):
        assert name in design
    assert {name: theme.get(name) for name in design} == design


def test_el_tema_no_agrega_valores_que_design_md_no_tiene():
    assert set(theme_tokens()) - set(design_tokens()) == set()
