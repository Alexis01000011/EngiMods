---
name: proponer-adr
description: Investiga y redacta un ADR en estado Propuesta en docs/decisiones/ para una decisión técnica o de proveedor de EngiMods (hosting, correo, estilos, una dependencia nueva como django-allauth), con opciones, costos con fuente y fecha, y una recomendación para que el equipo decida. Úsala cuando una historia dependa de una decisión abierta, o la persona pida comparar opciones o "hacer el ADR de X".
---

# Proponer un ADR

Los agentes no eligen proveedores ni enfoques (`AGENTS.md` sección 8): preparan la decisión para que el equipo la tome.

## Antes de empezar

- Si la decisión es técnica o de proveedor, va en un ADR. Si es de negocio (precios, días de acceso, juegos del piloto, textos legales, quién revisa), no: pregúntale a la persona y, si te lo pide, anótala en "Hipótesis y decisiones abiertas" de `docs/BACKLOG.md`.
- Lee `docs/decisiones/README.md` (plantilla e índice) y los ADR existentes para no contradecirlos.
- Junta las restricciones:
  - El gasto del piloto tiene un tope de MXN 1,500 en total (`docs/negocio.md`).
  - El stack está en el ADR 0001: Django 5.2, PostgreSQL en producción, uv.
  - El equipo son 3 estudiantes y la entrega es alrededor del 1 de diciembre de 2026.
  - El público está en México.

## Investigar

- Compara de 2 a 4 opciones reales, incluida la más simple (a veces es "todavía no").
- Toma costos y límites solo de la página oficial del proveedor, con enlace y fecha de consulta (AAAA-MM-DD). Si no pudiste verificar un dato, escribe "sin verificar"; nunca lo estimes de memoria.
- Para cada opción anota:
  - Costo mensual en MXN, y en USD si cobra en dólares.
  - Capa gratuita y sus límites.
  - Qué historias desbloquea y cuánto cuesta configurarla.
  - Compatibilidad con Django y PostgreSQL.
  - Qué tan fácil es cambiar después.

## Escribir

- Crea `docs/decisiones/NNNN-titulo-corto.md` con el siguiente número libre y la plantilla del README. Usa `Estado: Propuesta` y `Historia: EM-0XX`.
- En "Decisión" escribe "Recomendación:" con el porqué, y deja claro que falta la decisión del equipo.
- Agrega la línea al índice de `docs/decisiones/README.md`.
- Abre el PR con título `Docs: propone el ADR NNNN sobre <tema>` y pídele a la persona que lo lleve al equipo.
- Si la persona lo autoriza, etiqueta con `decision-pendiente` las issues que esperan la decisión.

## Cuando el equipo decida

- Cambia a `Estado: Aceptada` y reescribe "Decisión" con lo elegido y la fecha.
- Quita la decisión de "Decisiones abiertas" en `AGENTS.md` sección 2 y de "Sigue abierto" en `docs/BACKLOG.md`.
- Quita `decision-pendiente` de las issues.
- Un ADR aceptado ya no se edita. Si después cambia la decisión, escribe uno nuevo y marca el anterior `Reemplazada por NNNN`.
