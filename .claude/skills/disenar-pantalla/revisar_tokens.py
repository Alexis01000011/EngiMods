"""Compara los tokens de DESIGN.md con las variables de referencia/engimods.css.

Uso: uv run python .claude/skills/disenar-pantalla/revisar_tokens.py

Revisa colores, esquinas y espacios: cada token de DESIGN.md debe existir como
variable CSS con el mismo valor (--color-<nombre>, --rounded-<nombre>,
--spacing-<nombre>) y la hoja no debe tener variables que DESIGN.md no declare.
Sale con código 1 si encuentra diferencias.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DESIGN = ROOT / "DESIGN.md"
CSS = Path(__file__).resolve().parent / "referencia" / "engimods.css"
GROUPS = {"colors": "color", "rounded": "rounded", "spacing": "spacing"}


def design_tokens() -> dict[str, str]:
    text = DESIGN.read_text(encoding="utf-8")
    front = text.split("---", 2)[1]
    tokens: dict[str, str] = {}
    group = None
    for line in front.splitlines():
        top = re.match(r"^([a-z-]+):\s*$", line)
        if top:
            group = top.group(1)
            continue
        if re.match(r"^\S", line):
            group = None
            continue
        item = re.match(r"^  ([a-z0-9-]+):\s*(.+?)\s*$", line)
        if group in GROUPS and item:
            value = item.group(2).strip("\"'")
            tokens[f"--{GROUPS[group]}-{item.group(1)}"] = value.lower()
    return tokens


def css_tokens() -> dict[str, str]:
    text = CSS.read_text(encoding="utf-8")
    pattern = r"(--(?:color|rounded|spacing)-[a-z0-9-]+):\s*([^;]+);"
    return {name: value.strip().lower() for name, value in re.findall(pattern, text)}


def main() -> int:
    design, css = design_tokens(), css_tokens()
    problems = []
    for name, value in design.items():
        if name not in css:
            problems.append(f"Falta {name} en engimods.css (DESIGN.md: {value})")
        elif css[name] != value:
            problems.append(f"{name}: DESIGN.md dice {value} y engimods.css {css[name]}")
    for name in css.keys() - design.keys():
        problems.append(f"{name} está en engimods.css pero no en DESIGN.md")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(design)} tokens coinciden entre DESIGN.md y engimods.css.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
