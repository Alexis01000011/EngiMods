"""Mantiene consistente docs/BACKLOG.md.

La fuente de verdad son las secciones de cada historia (línea "Tipo: ..." y
"Depende de: ..."). El índice, las olas, el resumen por épica y el orden
sugerido se derivan de ellas.

    uv run python scripts/backlog.py           # revisa (lo corre la CI)
    uv run python scripts/backlog.py --write   # regenera lo derivado y revisa
"""

import argparse
import re
import sys
from collections import OrderedDict
from pathlib import Path

BACKLOG = Path(__file__).resolve().parent.parent / "docs" / "BACKLOG.md"
HISTORIAS = "\n## Historias\n"
DECISIONES = "\n## Hipótesis y decisiones abiertas\n"


def parse(text):
    """Devuelve (épicas, historias) leídas de la sección "## Historias"."""
    hist = text.split(HISTORIAS, 1)[1].split(DECISIONES, 1)[0]
    epics = OrderedDict()
    stories = OrderedDict()
    epic = None
    for block in re.split(r"(?m)^(?=### E\d+ |#### EM-\d+)", hist):
        m = re.match(r"### (E\d+) (.+)", block)
        if m:
            epic = m.group(1)
            epics[epic] = m.group(2).strip()
            continue
        m = re.match(r"#### (EM-\d+)", block)
        if not m:
            continue
        meta_line = re.search(r"(?m)^Tipo: .+$", block).group(0)
        meta = dict(kv.split(": ", 1) for kv in meta_line.split(" · "))
        deps = re.search(r"(?m)^Depende de: (.+)$", block)
        stories[m.group(1)] = {
            "epic": epic,
            "title": re.search(r"(?m)^\*\*(.+?)\*\*$", block).group(1),
            "meta_line": meta_line,
            "prio": meta["Prioridad"],
            "pts": int(meta["Puntos"]) if "Puntos" in meta else None,
            "done": meta.get("Estado") == "Hecho",
            "issue": meta["Issue"],
            "deps": re.findall(r"EM-\d+", deps.group(1)) if deps else [],
        }
    return epics, stories


def compute_waves(stories):
    """Ola = 0 si está hecha; si no, 1 + la ola más alta de sus dependencias."""
    waves = {}

    def wave(sid, stack=()):
        if sid in waves:
            return waves[sid]
        if sid in stack:
            raise SystemExit(f"Ciclo de dependencias: {' -> '.join(stack + (sid,))}")
        s = stories[sid]
        if s["prio"] == "Later":
            waves[sid] = None
        elif s["done"]:
            waves[sid] = 0
        else:
            waves[sid] = 1 + max((wave(d, stack + (sid,)) for d in s["deps"]), default=0)
        return waves[sid]

    for sid, s in stories.items():
        for d in s["deps"]:
            if d not in stories:
                raise SystemExit(f"{sid} depende de {d}, que no existe")
        wave(sid)
    return waves


def link(sid):
    return f"[{sid}](#{sid.lower()})"


def regenerate(text):
    """Recalcula olas, índice, resumen y orden sugerido. Devuelve el texto nuevo."""
    epics, stories = parse(text)
    waves = compute_waves(stories)
    ordered = sorted(stories, key=lambda sid: int(sid.split("-")[1]))

    head, rest = text.split(HISTORIAS, 1)
    hist, tail = rest.split(DECISIONES, 1)

    for sid, s in stories.items():
        if waves[sid] is None:
            continue
        start = hist.index(f"#### {sid}\n")
        i = hist.index(s["meta_line"], start)
        new_meta = re.sub(r"Ola: \d+", f"Ola: {waves[sid]}", s["meta_line"])
        hist = hist[:i] + new_meta + hist[i + len(s["meta_line"]) :]

    rows = [
        "| ID | Issue | Título | Épica | Prioridad | Pts | Ola | Depende de | Estado |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for sid in ordered:
        s = stories[sid]
        m = re.match(r"\[#(\d+)\]\(([^)]+)\)", s["issue"])
        rows.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                link(sid),
                f"[#{m.group(1)}]({m.group(2)})" if m else "por crear",
                s["title"],
                s["epic"],
                s["prio"],
                "-" if s["pts"] is None else s["pts"],
                "-" if waves[sid] is None else waves[sid],
                ", ".join(s["deps"]) or "-",
                "Hecho" if s["done"] else "Pendiente",
            )
        )
    head = re.sub(
        r"(?ms)^\| ID \| Issue \|.*?(?=\n\n|\Z)", lambda _: "\n".join(rows), head, count=1
    )

    summary = [
        "| Épica | Nombre | Historias R1 | Puntos R1 (Must) | Puntos R1 (total) | Historias R2 |",
        "|---|---|---|---|---|---|",
    ]
    total = [0, 0, 0, 0]
    for epic, name in epics.items():
        ss = [s for s in stories.values() if s["epic"] == epic]
        r1 = [s for s in ss if s["prio"] != "Later"]
        counts = [
            len(r1),
            sum(s["pts"] for s in r1 if s["prio"] == "Must"),
            sum(s["pts"] for s in r1),
            len(ss) - len(r1),
        ]
        total = [a + b for a, b in zip(total, counts, strict=True)]
        summary.append(f"| {epic} | {name} | " + " | ".join(map(str, counts)) + " |")
    summary.append("| | **Total** | " + " | ".join(f"**{x}**" for x in total) + " |")
    head = re.sub(
        r"(?ms)^\| Épica \| Nombre \|.*?(?=\n\n)", lambda _: "\n".join(summary), head, count=1
    )

    lines = []
    for n in range(max(w for w in waves.values() if w is not None) + 1):
        items = ", ".join(
            f"{link(sid)} {stories[sid]['title']} ({stories[sid]['prio']})"
            for sid in ordered
            if waves[sid] == n
        )
        lines.append(f"**{'Ola 0 (hecho)' if n == 0 else f'Ola {n}'}:** {items}")
    head = re.sub(
        r"(?ms)(^## Orden sugerido para R1 \(olas por dependencias\)\n\n).*?(?=\n\n## )",
        lambda m: m.group(1) + "\n\n".join(lines),
        head,
        count=1,
    )

    return head + HISTORIAS + hist + DECISIONES + tail


def check_recorte(text):
    """Revisa la sección del recorte de semestre, si existe."""
    if "\n## Recorte para la entrega de semestre\n" not in text:
        return []
    _, stories = parse(text)
    waves = compute_waves(stories)
    cut = text.split("\n## Recorte para la entrega de semestre\n", 1)[1]
    cut = cut.split("\n## ", 1)[0]
    errors = []

    def segment(heading):
        m = re.search(rf"(?ms)^### {heading}.*?(?=^### |\Z)", cut)
        if not m:
            errors.append(f"Recorte: falta la sección '### {heading}'")
            return ""
        return m.group(0)

    blocks = {}
    for name in ("A", "B", "C"):
        seg = segment(f"Bloque {name}:")
        blocks[name] = re.findall(r"\[(EM-\d+)\]\(#em-\d+\)", seg)
        declared = re.search(r"\((\d+) pts", seg.splitlines()[0]) if seg else None
        pts = sum(stories[s]["pts"] or 0 for s in blocks[name])
        if declared and int(declared.group(1)) != pts:
            errors.append(f"Recorte: el bloque {name} dice {declared.group(1)} pts y suma {pts}")
        if name == "A":
            for m in re.finditer(r"(?m)^\| (\d+) \| (.+) \| (\d+) \|$", seg):
                ids = re.findall(r"EM-\d+", m.group(2))
                for sid in ids:
                    if waves[sid] != int(m.group(1)):
                        errors.append(
                            f"Recorte: {sid} está en la fila de la ola {m.group(1)}, "
                            f"pero su ola es {waves[sid]}"
                        )
                row_pts = sum(stories[s]["pts"] for s in ids)
                if row_pts != int(m.group(3)):
                    errors.append(
                        f"Recorte: la ola {m.group(1)} dice {m.group(3)} pts y suma {row_pts}"
                    )

    fuera_seg = segment("Fuera del semestre")
    fuera = re.findall(r"EM-\d+", "\n".join(ln for ln in fuera_seg.splitlines() if ln[:2] == "- "))

    listed = blocks["A"] + blocks["B"] + blocks["C"] + fuera
    repeated = sorted({s for s in listed if listed.count(s) > 1})
    if repeated:
        errors.append(f"Recorte: historias en más de un lugar: {', '.join(repeated)}")
    pending = {s for s, v in stories.items() if v["prio"] != "Later" and not v["done"]}
    if missing := sorted(pending - set(listed)):
        errors.append(f"Recorte: historias de R1 que no aparecen: {', '.join(missing)}")
    if extra := sorted(set(listed) - pending):
        errors.append(f"Recorte: historias que no son de R1 pendientes: {', '.join(extra)}")

    allowed = {s for s, v in stories.items() if v["done"]}
    for name in ("A", "B", "C"):
        allowed |= set(blocks[name])
        for sid in blocks[name]:
            if outside := sorted(set(stories[sid]["deps"]) - allowed):
                errors.append(
                    f"Recorte: {sid} (bloque {name}) depende de {', '.join(outside)}, "
                    "que no está en su bloque ni en uno anterior"
                )
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="regenera lo derivado")
    args = parser.parse_args()

    text = BACKLOG.read_text(encoding="utf-8")
    new = regenerate(text)
    errors = []
    if args.write:
        if new != text:
            BACKLOG.write_text(new, encoding="utf-8")
            print("docs/BACKLOG.md regenerado.")
    elif new != text:
        errors.append(
            "El índice, las olas, el resumen o el orden sugerido no coinciden con las "
            "secciones de las historias. Corre: uv run python scripts/backlog.py --write"
        )
    errors += check_recorte(new)

    if errors:
        print("\n".join(f"- {e}" for e in errors), file=sys.stderr)
        sys.exit(1)
    print("docs/BACKLOG.md consistente.")


if __name__ == "__main__":
    main()
