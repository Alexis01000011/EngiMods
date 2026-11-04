---
name: tomar-historia
description: Toma, implementa y entrega una historia EM-### de EngiMods de punta a punta (elegir, asignar, rama, código con pruebas, PR) siguiendo AGENTS.md. Úsala cuando la persona diga "implementa EM-0XX", "toma la siguiente historia", "¿qué sigue?", "empieza o continúa EM-0XX", o pida abrir el PR de una historia.
---

# Tomar una historia

Esta skill es `AGENTS.md` (secciones 5 a 8) en pasos. Si algo choca, gana `AGENTS.md`.

## 1. Elegir

- Si la persona dio un ID, úsalo. Si pidió "la siguiente", ve a la sección "Recorte para la entrega de semestre" de `docs/BACKLOG.md`: bloque A por ola, luego B, luego C. No tomes nada de "Fuera del semestre" ni de R2 salvo que la persona lo pida.
- Lee completa la sección `#### EM-0XX`: criterios, "Depende de" y notas.
- Comprueba que cada dependencia esté cerrada:
  `gh issue list --state all --search "EM-0YY in:title" --json number,state,title`.
  Si alguna sigue abierta, para y díselo a la persona; propón otra historia de la misma ola.
- Si la historia necesita una decisión abierta (sección "Hipótesis y decisiones abiertas" del backlog, `AGENTS.md` sección 2 o etiqueta `decision-pendiente`), no la inventes. Si es técnica o de proveedor, usa la skill `proponer-adr`; si es de negocio, pregúntale a la persona.

## 2. Reclamar

- `gh issue view <n> --json assignees,state`. Si la tiene otra persona, elige otra historia.
- Asígnala a tu persona antes de escribir código: `gh issue edit <n> --add-assignee @me`. Díselo.
- Rama desde `main` actualizado:
  `git switch main && git pull --ff-only && git switch -c em-0XX-descripcion-corta`.

## 3. Implementar

- Lee en `docs/arquitectura.md` qué app es dueña de los modelos que vas a tocar y las reglas del modelo de datos. Si la app no existe todavía: `uv run python manage.py startapp <app>` y regístrala en `INSTALLED_APPS`.
- Haz solo lo que piden los criterios. Si encuentras trabajo extra, anótalo como historia propuesta en el PR.
- Por cada criterio de comportamiento escribe al menos una prueba en `<app>/tests/test_*.py`. Incluye a quien no debe poder: anónimo, alumno sin acceso vigente, usuario que no es tutor.
- Reglas que más se rompen:
  - `settings.AUTH_USER_MODEL` o `get_user_model()`, nunca `django.contrib.auth.models.User`.
  - Dinero en centavos enteros de MXN, estados con `TextChoices`, `on_delete=PROTECT` en pagos e inscripciones.
  - Precios, cupos, días de acceso, enlaces y textos legales son datos (modelo o settings), no constantes.
  - Nada escrito para un juego en particular.
  - Textos visibles en español con `gettext_lazy as _`; URLs en español con `app_name` y `reverse()`.
  - Migraciones solo de tus apps. Nunca edites una que ya esté en `main` (el hook lo bloquea).
  - Variable de entorno nueva: agrégala a `.env.example` con un comentario.
- Si cambian el alcance o los criterios, actualiza la sección en `docs/BACKLOG.md` en el mismo PR con la skill `cambiar-backlog`.

## 4. Verificar

No abras el PR si alguno de estos falla:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run python manage.py makemigrations --check --dry-run
uv run pytest
```

Si la historia tiene pantallas, ábrelas con `uv run python manage.py runserver`, también en ancho de teléfono. Si no pudiste verlas, dilo en el PR.

## 5. Entregar

- Marca la historia como hecha en `docs/BACKLOG.md`, en el mismo PR: `Estado: Hecho` antes de `Issue:`, criterios en `[x]` y `uv run python scripts/backlog.py --write`. Así, al mezclarse el PR, la issue se cierra y el backlog ya lo dice. Si al actualizar tu rama hay conflicto en el índice del backlog, quédate con cualquiera de las dos versiones y vuelve a correr el script: el índice se regenera desde las secciones.
- Commits en español e imperativo con el ID: `EM-0XX: agrega el modelo de inscripción`.
- `git push -u origin em-0XX-descripcion-corta`.
- Llena `.github/pull_request_template.md` en un archivo temporal y crea el PR:
  `gh pr create --title "EM-0XX: <título de la historia>" --body-file <archivo>`.
  - `Closes #<n>`.
  - Copia los criterios del backlog y marca cada uno con la prueba que lo cubre.
  - En "Supuestos y pendientes" lista los datos de negocio que dejaste configurables y lo que no pudiste verificar.
- No mezcles el PR por tu cuenta. Avísale a la persona que está listo; ella decide si se mezcla ya o si primero se lo pide revisar a alguien del equipo (sugerido; puede usar la skill `revisar-pr`). Si te pide explícitamente mezclarlo, revisa que la CI esté en verde (`gh pr checks <n>`) y usa `gh pr merge <n> --squash --delete-branch`.
