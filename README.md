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
uv run python manage.py tailwind runserver
```

Abre http://localhost:8000. `tailwind runserver` levanta Django y recompila los estilos al guardar. La primera vez descarga el CLI de Tailwind (unos 100 MB), así que necesita internet y puede tardar unos minutos. Si prefieres `runserver`, compila antes con `uv run python manage.py tailwind build`. Para desplegar, corre `tailwind build` antes de `collectstatic`. La identidad visual está en [`DESIGN.md`](DESIGN.md). Pruebas: `uv run pytest`. Lint y formato: `uv run ruff check . && uv run ruff format .`.

## Datos de ejemplo

Para tener contenido con el que trabajar sin capturarlo a mano:

```bash
uv run python manage.py seed_demo
```

Crea dos juegos con su versión actual y su entorno de modding, un curso publicado por juego con dos módulos y cuatro lecciones (cada una con su "probado con"), y tres cuentas de ejemplo: `tutor@example.com` (tutora), `alumno1@example.com` y `alumno2@example.com` (alumnos). La contraseña de las tres es `demo12345`. Son datos de desarrollo: no uses esas cuentas fuera de tu máquina.

Se puede correr varias veces: actualiza lo que ya existe y no duplica nada. No borra datos que hayas capturado.

## Cómo colaborar

1. Lee [`AGENTS.md`](AGENTS.md): reglas del proyecto para personas y agentes (Claude Code, Codex). Si usas Codex, abre `/hooks` y aprueba los hooks del proyecto; las skills y hooks están en la sección 10.
2. Elige una historia en [`docs/BACKLOG.md`](docs/BACKLOG.md) y asígnate su issue.
3. Rama `em-0XX-descripcion`, PR con `Closes #<issue>`. Se sugiere que otra persona lo revise antes de mezclarlo.

## Documentación

- [`docs/BACKLOG.md`](docs/BACKLOG.md): product backlog.
- [`docs/arquitectura.md`](docs/arquitectura.md): apps, modelos y reglas.
- [`docs/negocio.md`](docs/negocio.md): modelo de negocio e hipótesis.
- [`docs/flujo-de-trabajo.md`](docs/flujo-de-trabajo.md): sprints, etiquetas y criterios.
- [`docs/stripe.md`](docs/stripe.md): Stripe en modo prueba y webhooks en local.
- [`docs/decisiones/`](docs/decisiones/): decisiones técnicas (ADR).
