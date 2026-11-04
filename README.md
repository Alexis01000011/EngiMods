# EngiMods

Academia en línea para aprender a crear mods de videojuegos aplicando ingeniería de software: Git, pruebas, calidad, documentación, publicación y mantenimiento. Cada lección indica con qué versión del juego fue probada y un tutor revisa lo que construye cada alumno.

Proyecto del Equipo 8 de Negocios Electrónicos, Ingeniería de Software, Universidad Autónoma de Zacatecas.

## Arranque rápido

Requisitos: Python 3.12+ y [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Alexis01000011/EngiMods.git
cd EngiMods
uv sync
git config core.hooksPath .githooks       # activa los git hooks del repo
cp .env.example .env
uv run python manage.py migrate
uv run python manage.py runserver
```

Abre http://localhost:8000. Pruebas: `uv run pytest`. Lint y formato: `uv run ruff check . && uv run ruff format .`.

## Cómo colaborar

1. Lee [`AGENTS.md`](AGENTS.md): reglas del proyecto para personas y agentes (Claude Code, Codex). Si usas Codex, abre `/hooks` y aprueba los hooks del proyecto; las skills y hooks están en la sección 10.
2. Elige una historia en [`docs/BACKLOG.md`](docs/BACKLOG.md) y asígnate su issue.
3. Rama `em-0XX-descripcion`, PR con `Closes #<issue>`, revisión de otra persona.

## Documentación

- [`docs/BACKLOG.md`](docs/BACKLOG.md): product backlog.
- [`docs/arquitectura.md`](docs/arquitectura.md): apps, modelos y reglas.
- [`docs/negocio.md`](docs/negocio.md): modelo de negocio e hipótesis.
- [`docs/flujo-de-trabajo.md`](docs/flujo-de-trabajo.md): sprints, etiquetas y criterios.
- [`docs/stripe.md`](docs/stripe.md): Stripe en modo prueba y webhooks en local.
- [`docs/decisiones/`](docs/decisiones/): decisiones técnicas (ADR).
