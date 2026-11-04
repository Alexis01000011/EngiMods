# Nota de traspaso para el agente en la nube

Dejada el 2026-11-04 por la sesión de Claude Code de Alexis. **Léela, y bórrala en el primer PR que abras** con un commit aparte: `Docs: borra la nota de traspaso`. No la copies a otro lado: lo que importa ya está en `AGENTS.md` y en `docs/BACKLOG.md`.

## Qué hay hecho

En `main` ya están EM-020, EM-021, EM-036, EM-041, EM-053, EM-060 y EM-061, además de lo anterior. Las issues de cada historia ya coinciden con el backlog.

## UX/UI: no la toques

La rama `ux-ui-estilos-design-md` ya está en GitHub y **está pendiente de revisión del equipo**. Trae un `DESIGN.md` (formato de Google Labs) y una actualización del ADR 0002 que propone Tailwind con `django-tailwind-cli`. Mientras el equipo no acepte el ADR 0002:

- No tomes EM-004 ni agregues estilos, CSS, frameworks ni fuentes.
- No edites esa rama ni copies su contenido a la tuya.
- Las pantallas nuevas van en HTML semántico simple sobre `templates/base.html`, como las que ya existen.

## Qué sigue (sin UX/UI)

Usa la skill `tomar-historia`. Las issues de abajo están libres y sus dependencias ya están cerradas:

1. **EM-062, marcar lección como completada (#41).** El modelo `LessonProgress` es de la app `enrollments` (ver `docs/arquitectura.md`). El panel `/mi-panel/` (EM-060) debe mostrar el porcentaje y enlazar a la siguiente lección pendiente. La vista de lección es `courses:lesson_detail`.
2. **EM-070, enviar una entrega (#43).** Crea la app `submissions`. La entrega se liga a la `Enrollment`, no solo al usuario. Los grupos (EM-050) no existen y están fuera del semestre: no agregues grupo; muévelo a EM-050 con la skill `cambiar-backlog`, como se hizo con EM-053, EM-041 y EM-060. La versión del juego y del entorno apuntan a los modelos de `catalog`.

Cuando EM-070 esté en `main`, siguen **EM-071 (cola de revisión, #44)** y **EM-072 (revisar con rúbrica, #45)**, que se pueden hacer en paralelo. Ambas son pantallas del tutor fuera del admin, con `accounts.permissions.tutor_required`.

Todo lo demás del bloque A espera decisiones del equipo: estilos (ADR 0002, la rama de arriba), hosting (ADR 0003) y correo (ADR 0004). No las tomes.

## Cosas que conviene saber

- **Inicio de sesión:** todavía no existe pantalla de login (EM-031). Las vistas con `login_required` redirigen a `/accounts/login/`, que da 404. En las pruebas usa `client.force_login`. No crees el login ni cambies `LOGIN_URL`.
- **Acceso vigente:** usa `Enrollment.objects.with_access()`. La regla de una sola inscripción vigente vive en `Enrollment.clean()`, no en la base de datos.
- **Mezclas:** las issues se asignan a Alexis. Abre el PR y detente; no lo mezcles salvo que Alexis te lo pida para ese PR.
- **Decisiones abiertas del equipo, que no debes inventar:** qué mostrar si un curso con inscritos vuelve a borrador, el texto legal de términos y devolución, y si el precio incluye IVA.
