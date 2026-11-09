#!/usr/bin/env bash
# Build de staging en Render (EM-005, ADR 0003). Lo llama render.yaml en cada despliegue.
# Pasos completos en docs/despliegue.md.
set -o errexit -o nounset -o pipefail

# Render instala uv cuando el repo tiene uv.lock, y su Python sale de .python-version.
uv sync --locked --no-dev

# Después de sincronizar se usa el Python de .venv directamente: es el mismo que arranca
# gunicorn, y no depende de que uv siga instalado.
.venv/bin/python manage.py tailwind build
.venv/bin/python manage.py collectstatic --no-input
# El plan gratuito no tiene paso previo al despliegue: las migraciones corren aquí.
.venv/bin/python manage.py migrate --no-input
