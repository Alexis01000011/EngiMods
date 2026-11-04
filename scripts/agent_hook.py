"""Hooks de agente compartidos por Claude Code y Codex.

Los llaman .claude/settings.json y .codex/hooks.json, que les pasan el evento
como JSON por stdin. Para bloquear una acción salen con código 2 y explican el
motivo en stderr; los dos agentes lo interpretan igual.

    python scripts/agent_hook.py session-start   # contexto al iniciar sesión
    python scripts/agent_hook.py pre-bash        # antes de cada comando de shell
    python scripts/agent_hook.py pre-edit        # antes de cada edición de archivo

Reglas que aplica: AGENTS.md, secciones 3, 5, 6 y 8.
"""

import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

SKILLS = "tomar-historia, revisar-pr, cambiar-backlog, proponer-adr"
HOOKS_PATH = ".githooks"


def git(cwd, *args):
    """Corre git y devuelve su salida, o None si falla."""
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def block(reason):
    print(reason, file=sys.stderr)
    sys.exit(2)


# --- Inicio de sesión ---------------------------------------------------------


def session_start(data):
    cwd = Path(data.get("cwd") or ".")
    root = git(cwd, "rev-parse", "--show-toplevel")
    if root is None:
        return
    branch = git(root, "branch", "--show-current") or "(HEAD separado)"
    lines = ["[EngiMods] Contexto de la sesión", f"- Rama: {branch}"]

    m = re.match(r"em-(\d{3})", branch)
    if branch == "main":
        lines.append(
            "- Estás en main. Antes de cambiar archivos crea una rama desde main "
            "actualizado (skill tomar-historia)."
        )
    elif m:
        sid = f"EM-{m.group(1)}"
        lines.append(f"- Historia de esta rama: {sid}. {story_summary(Path(root), sid)}")

    if git(root, "config", "core.hooksPath") != HOOKS_PATH:
        lines.append(
            "- AVISO: los git hooks del repo no están activados en esta copia. "
            f"Recuérdale a tu humano que corra: git config core.hooksPath {HOOKS_PATH}"
        )
    if shutil.which("uv") is None:
        lines.append(
            "- AVISO: uv no está instalado; no podrás correr ruff, pruebas ni el "
            "chequeo de migraciones. Recuérdale a tu humano instalarlo (README)."
        )
    lines.append(f"- Skills del repo: {SKILLS}.")
    print("\n".join(lines))


def story_summary(root, sid):
    """Título y dependencias de la historia, leídos de docs/BACKLOG.md."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from backlog import parse

        _, stories = parse((root / "docs" / "BACKLOG.md").read_text(encoding="utf-8"))
    except Exception:
        return "No pude leer docs/BACKLOG.md."
    s = stories.get(sid)
    if s is None:
        return "No aparece en docs/BACKLOG.md; revisa el nombre de la rama."
    deps = ", ".join(s["deps"]) or "ninguna"
    return f'"{s["title"]}" ({s["prio"]}, {s["pts"]} pts). Depende de: {deps}.'


# --- Comandos de shell --------------------------------------------------------


def pre_bash(data):
    command = data.get("tool_input", {}).get("command", "")
    if isinstance(command, list):
        # Codex puede mandar el comando como argv, por ejemplo ["bash", "-lc", "..."].
        command = shlex.join(command)
    cwd = Path(data.get("cwd") or ".")
    for segment in segments(command):
        reason = check_segment(segment, cwd)
        if reason:
            block(reason)


def segments(command):
    """Divide el comando en comandos simples (separados por &&, ||, ;, | y saltos)."""
    try:
        lexer = shlex.shlex(command.replace("\n", ";"), posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return [command.split()]
    result = [[]]
    for tok in tokens:
        if tok and set(tok) <= set(";&|()"):
            result.append([])
        else:
            result[-1].append(tok)
    return [s for s in result if s]


def check_segment(tokens, cwd):
    while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
        tokens = tokens[1:]
    if not tokens:
        return None
    if tokens[0] in ("bash", "sh", "zsh") and len(tokens) > 2 and tokens[1] in ("-c", "-lc"):
        for segment in segments(tokens[2]):
            if reason := check_segment(segment, cwd):
                return reason
        return None
    if tokens[0] == "git":
        return check_git(tokens[1:], cwd)
    return None


def check_git(args, cwd):
    # Opciones globales de git: -C <dir>, -c <clave=valor>, --no-pager, etc.
    while args and args[0].startswith("-"):
        opt = args.pop(0)
        if opt == "-C" and args:
            cwd = cwd / args.pop(0)
        elif opt == "-c" and args:
            if args.pop(0).lower().startswith("core.hookspath"):
                return hooks_bypass()
    if not args:
        return None
    sub, args = args[0], args[1:]

    if "--no-verify" in args or (sub == "commit" and any(short_flag(a, "n") for a in args)):
        return hooks_bypass()
    if sub == "config":
        keys = [i for i, a in enumerate(args) if a.lower() == "core.hookspath"]
        value = args[keys[0] + 1 : keys[0] + 2] if keys else []
        unset = bool({"--unset", "--unset-all", "unset"} & set(args))
        if keys and (unset or value not in ([], [HOOKS_PATH])):
            return hooks_bypass()
    if sub == "push":
        return check_push(args, cwd)
    return None


def short_flag(arg, letter):
    return bool(re.fullmatch(r"-[A-Za-z]+", arg)) and letter in arg


def hooks_bypass():
    return (
        "Bloqueado: no te saltes ni desactives los git hooks del repo. Si un hook falla, "
        "corrige lo que reporta; si crees que el hook está mal, díselo a tu humano."
    )


def check_push(args, cwd):
    if "--force" in args or any(short_flag(a, "f") for a in args):
        return (
            "Bloqueado: no uses git push --force. Si reescribiste tu propia rama, usa "
            "git push --force-with-lease; nunca sobre ramas ajenas (AGENTS.md, sección 8)."
        )
    if any(a in ("--all", "--mirror") for a in args):
        return "Bloqueado: sube solo tu rama, no --all ni --mirror."
    positional = [a for a in args if not a.startswith("-")]
    refspecs = positional[1:]
    if any(r.startswith("+") for r in refspecs):
        return "Bloqueado: un refspec con + es un push forzado. Usa --force-with-lease."
    current = git(cwd, "branch", "--show-current")
    targets = [r.split(":")[-1] for r in refspecs]
    targets = [current if t == "HEAD" else t for t in targets] or [current]
    if any(t in ("main", "refs/heads/main") for t in targets):
        return (
            "Bloqueado: no se hace push directo a main. Sube tu rama "
            "(git push -u origin <rama>) y abre un PR (AGENTS.md, sección 5)."
        )
    return None


# --- Ediciones de archivos ----------------------------------------------------


def pre_edit(data):
    cwd = Path(data.get("cwd") or ".")
    root = git(cwd, "rev-parse", "--show-toplevel")
    if root is None:
        return
    root = Path(root).resolve()
    for path in edited_paths(data.get("tool_input", {})):
        full = (cwd / path).resolve()
        try:
            rel = full.relative_to(root).as_posix()
        except ValueError:
            continue
        if reason := check_path(rel, root):
            block(reason)


def edited_paths(tool_input):
    """Rutas que toca la edición, en el formato de Claude Code o de apply_patch (Codex)."""
    paths = [tool_input[k] for k in ("file_path", "notebook_path", "path") if tool_input.get(k)]
    for value in tool_input.values():
        if isinstance(value, str):
            paths += re.findall(
                r"(?m)^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+?)\s*$", value
            )
    return paths


def check_path(rel, root):
    name = rel.rsplit("/", 1)[-1]
    if rel == "uv.lock":
        return (
            "Bloqueado: no edites uv.lock a mano. Usa uv add, uv remove o uv lock "
            "(AGENTS.md, sección 3)."
        )
    if name == ".env":
        return (
            "Bloqueado: .env es local y puede tener secretos. Si hace falta una variable "
            "nueva, agrégala a .env.example con un comentario y pídele a tu humano que "
            "la copie a su .env."
        )
    if re.search(r"(^|/)migrations/[^/]+\.py$", rel) and name != "__init__.py":
        base = "origin/main" if git(root, "rev-parse", "-q", "--verify", "origin/main") else "main"
        if git(root, "cat-file", "-e", f"{base}:{rel}") is not None:
            return (
                f"Bloqueado: {rel} ya está en main y no se edita. Cambia el modelo y genera "
                "una migración nueva con makemigrations (AGENTS.md, sección 6)."
            )
    return None


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    raw = "" if sys.stdin.isatty() else sys.stdin.buffer.read().decode("utf-8", "replace")
    data = json.loads(raw) if raw.strip() else {}
    handlers = {"session-start": session_start, "pre-bash": pre_bash, "pre-edit": pre_edit}
    if len(sys.argv) != 2 or sys.argv[1] not in handlers:
        sys.exit(f"Uso: agent_hook.py {{{','.join(handlers)}}}")
    handlers[sys.argv[1]](data)


if __name__ == "__main__":
    main()
