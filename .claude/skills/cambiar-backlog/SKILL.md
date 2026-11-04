---
name: cambiar-backlog
description: Agrega o cambia historias en docs/BACKLOG.md de EngiMods (criterios, dependencias, prioridad, puntos, bloque del recorte) sin desincronizar el índice, las olas, el resumen, el recorte de semestre ni las issues de GitHub. Úsala cuando la persona pida agregar una historia, cambiar criterios o dependencias, mover algo de bloque, o cuando una implementación cambie el alcance de su historia.
---

# Cambiar el backlog

`docs/BACKLOG.md` define el alcance. La fuente de verdad son las secciones `#### EM-###`. El índice, la ola de cada historia, el resumen por épica y el orden sugerido se generan con `scripts/backlog.py`; no los edites a mano.

## Formato de una historia

```markdown
#### EM-0XX

**Título corto**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 1 · Issue: por crear

> Como **rol**, quiero qué, para qué.

Criterios de aceptación:

- [ ] Verificable, uno por línea.

Depende de: [EM-003](#em-003), [EM-010](#em-010)

Nota: contexto o decisión que explica la historia.
```

- `Tipo`: `Historia de usuario` (lleva la línea "Como...") o `Técnica` (sin ella).
- R1 lleva `Prioridad` Must, Should o Could, `Puntos` (1, 2, 3, 5 u 8) y `Ola`. R2 lleva `Prioridad: Later`, sin puntos ni ola.
- `Ola`: escribe cualquier número; el script la recalcula.
- ID: el siguiente libre en la decena de su épica (EM-03X es E3). Si la decena está llena, pregúntale a la persona; no inventes otro esquema.
- Al terminar una historia: `Estado: Hecho` antes de `Issue:` y criterios en `[x]`.

## Pasos

1. Edita o agrega las secciones.
2. Regenera lo derivado: `uv run python scripts/backlog.py --write`.
3. Si el script reporta problemas del recorte (historia que no aparece en ningún bloque, puntos que no suman, dependencia en un bloque posterior), decide con la persona dónde va la historia y corrige a mano la sección "Recorte para la entrega de semestre": la tabla del bloque A tiene una fila por ola con sus puntos y cada bloque declara su total en el título.
4. Repite `uv run python scripts/backlog.py` hasta que diga "consistente". La CI corre el mismo chequeo.
5. Si cambió qué entra al semestre, revisa también `AGENTS.md` sección 2.

## Issues de GitHub

Crear o editar issues es visible para todo el equipo: confírmalo con la persona antes.

- **Historia nueva:** crea la issue con el cuerpo de la plantilla `.github/ISSUE_TEMPLATE/historia.yml` (Historia, Criterios de aceptación, Depende de, Notas):
  `gh issue create --title "EM-0XX: <título>" --label E3,must,historia --body-file <archivo>`.
  Después cambia `Issue: por crear` por `Issue: [#N](https://github.com/Alexis01000011/EngiMods/issues/N)` y vuelve a correr el script.
- **Criterios cambiados:** el cuerpo de la issue copia los criterios, así que actualízalo: `gh issue edit <n> --body-file <archivo>`.
- Etiquetas: épica `E0` a `E10`, prioridad `must`, `should`, `could` o `later`, y `historia` o `tecnica`. Ver `docs/flujo-de-trabajo.md`.

## Commit

- Dentro del PR de una historia, va con sus commits: `EM-0XX: ajusta los criterios ...`.
- Si solo cambia el backlog: `Docs: agrega EM-0XX <título>` en su propio PR.
