---
name: revisar-pr
description: Revisa un PR de EngiMods contra los criterios de su historia, la Definition of Done y las reglas de AGENTS.md y docs/arquitectura.md, y entrega un veredicto con hallazgos concretos. Úsala cuando la persona pida "revisa el PR #N", "¿está listo este PR?", "checa la rama de X", o quiera revisar su propio trabajo antes de pedir revisión.
---

# Revisar un PR

Tu trabajo es que la persona revisora decida rápido y con evidencia. Tú no apruebas; eso lo hace una persona. Mezcla solo si la persona te lo pide explícitamente para ese PR (`AGENTS.md`, sección 8).

## 1. Reunir contexto

```bash
gh pr view <n> --json title,body,author,headRefName,files
gh pr diff <n>
gh pr checks <n>
```

- Saca el ID del título y lee su sección en `docs/BACKLOG.md`: criterios, dependencias y notas.
- Lee en `docs/arquitectura.md` la fila de la app que toca.
- Para correr el código sin mover la rama de la persona, usa un worktree aparte:
  `git fetch origin pull/<n>/head:pr-<n> && git worktree add ../pr-<n> pr-<n>`.
  Ahí corre `uv sync` y los cuatro comandos de la CI. Al terminar, `git worktree remove ../pr-<n>`.

## 2. Revisar, en este orden

1. **Criterios.** Uno por uno: ¿está implementado y qué prueba lo cubre? Un criterio sin prueba es un hallazgo.
2. **Alcance.** Una sola historia, sin refactors de código ajeno. Si toca otra app, el PR debe explicarlo.
3. **Permisos.** Cada vista con contenido de pago o de tutor está protegida (`login_required`, acceso vigente, la protección de tutor de `accounts`) y hay pruebas de quién no debe entrar.
4. **Reglas del modelo** (`AGENTS.md` sección 6 y `docs/arquitectura.md`): `AUTH_USER_MODEL`, dinero en centavos, `TextChoices`, `PROTECT` en pagos e inscripciones, datos de negocio como datos, nada específico de un juego, textos en español con `gettext_lazy`.
5. **Migraciones.** Solo de las apps de la historia y ninguna migración de `main` editada. Si otro PR abierto toca la misma app, avisa del posible choque de numeración.
6. **Seguridad.** Markdown sanitizado, webhooks que verifican firma, nada de llaves ni datos de pago en logs, nada de `.env`, llaves o datos personales reales en código o fixtures.
7. **Definition of Done** (`AGENTS.md` sección 7): plantilla de PR llena, `.env.example` al día, ADR si hubo decisión técnica o de proveedor, la historia marcada como hecha en `docs/BACKLOG.md` (`Estado: Hecho` y criterios en `[x]`) y su sección actualizada si cambió el alcance.
8. **Supuestos.** Un precio, texto legal, plazo o regla de negocio inventados son bloqueantes. Deben quedar configurables y listados en el PR.

## 3. Reportar

Usa este formato:

```
Veredicto: Listo para aprobar | Necesita cambios | Bloqueado por una decisión

Criterios
- [x] <criterio>: cubierto por accounts/tests/test_tutor.py::test_no_tutor_recibe_403
- [ ] <criterio>: no hay prueba / no está implementado

Hallazgos
1. [bloqueante] courses/views.py:42: qué pasa, por qué importa y cómo arreglarlo.
2. [sugerencia] ...
```

- Bloqueante es lo que rompe un criterio, una regla de `AGENTS.md` o la seguridad. Lo demás es sugerencia.
- Cita archivo y línea. No inventes problemas para llenar la lista; si está bien, dilo.
- Publica en GitHub solo si la persona lo pide: `gh pr review <n> --comment --body-file <archivo>`. No uses `--approve`; la aprobación la da la persona revisora.
