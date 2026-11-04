# Flujo de trabajo

## Dónde vive cada cosa

- **`docs/BACKLOG.md`** define el alcance: historias, criterios de aceptación, prioridad, dependencias. Se cambia por PR.
- **GitHub Issues** llevan el estado: una issue por historia, con el ID `EM-###` en el título. Abierta, asignada o cerrada.
- **Milestones:** `R1 Piloto` y `R2 Post-piloto`. Mientras esté vigente el recorte de semestre, las issues de los bloques A y B están en `Semestre` en lugar de `R1 Piloto`, porque una issue solo puede tener un milestone (ver `docs/BACKLOG.md`). Al cerrar el semestre, las que sigan abiertas regresan a `R1 Piloto`. Si el equipo usa sprints, se crea un milestone por sprint (`Sprint 1`, `Sprint 2`...) y se mueven ahí las issues comprometidas.

## Etiquetas

| Etiqueta | Uso |
|---|---|
| `E0` a `E10` | Épica a la que pertenece la historia |
| `must`, `should`, `could`, `later` | Prioridad MoSCoW |
| `historia` / `tecnica` | Historia de usuario o trabajo técnico |
| `bloqueada` | Tiene una dependencia abierta o una decisión pendiente |
| `decision-pendiente` | Necesita que el equipo decida algo antes de implementarse |
| `bug` | Defecto en algo ya entregado |

## Sprints (propuesta)

La duración y la capacidad las decide el equipo. Propuesta inicial: sprints de dos semanas.

1. **Planeación:** se eligen historias de la ola más baja disponible del backlog, cuidando que cumplan la Definition of Ready. Se ajustan los puntos si hace falta.
2. **Durante el sprint:** cada persona tiene una historia a la vez, asignada en su issue.
3. **Revisión:** se muestra lo mezclado en `main` (o en staging cuando exista).
4. **Retrospectiva y refinamiento:** se actualiza `docs/BACKLOG.md` con lo aprendido.

Los puntos del backlog son estimaciones iniciales. La velocidad real se mide después de los primeros sprints; antes de eso no hay base para prometer fechas.

## Definition of Ready

Una historia puede entrar a un sprint cuando:

- Sus dependencias están cerradas o se terminarán antes en el mismo sprint.
- Sus criterios de aceptación son verificables.
- No depende de una decisión abierta (si depende, lleva `decision-pendiente` y se resuelve primero).
- Tiene estimación acordada por el equipo.

## Definition of Done

Está en `AGENTS.md`, sección 7. Es la misma para personas y agentes.

## Trabajar con agentes (Claude Code, Codex)

- El agente trabaja para una persona; la issue se asigna a esa persona.
- Al empezar una sesión, el agente lee `AGENTS.md` (Claude Code lo recibe por `CLAUDE.md`).
- Pídele al agente una historia concreta por ID: "Implementa EM-010 siguiendo AGENTS.md", o usa la skill: `/tomar-historia EM-010` en Claude Code, `$tomar-historia EM-010` en Codex. Las demás skills y los hooks están en `AGENTS.md`, sección 10.
- Revisa el PR del agente como revisarías el de una persona. Que la CI pase no es suficiente.

## Agregar o cambiar historias

La skill `cambiar-backlog` hace estos pasos.

1. Edita `docs/BACKLOG.md`: usa el siguiente ID libre de la épica, con el mismo formato (historia, criterios, depende de, notas).
2. Corre `uv run python scripts/backlog.py --write`: recalcula las olas, el índice, el resumen y el orden sugerido, y revisa el recorte de semestre. La CI corre el mismo chequeo.
3. Crea la issue con la plantilla "Historia" y el mismo ID en el título.
4. Si cambian criterios de una historia existente, actualiza también su issue.
