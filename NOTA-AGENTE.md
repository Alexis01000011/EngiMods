# Nota de traspaso: deuda de diseño en las pantallas existentes

Dejada el 2026-11-04 por la sesión de Claude Code de Alexis. **Léela completa antes de empezar y bórrala en el primer PR que abras**, con un commit aparte: `Docs: borra la nota de traspaso`. Lo que deba quedar (la historia y sus criterios) va en `docs/BACKLOG.md`, no en otro archivo.

## Qué es esta tarea y por qué existe

Es una **tarea excepcional que no está en el backlog**. Alexis la aprobó el 2026-11-04 como deuda técnica.

- La identidad visual se decidió tarde. Mientras el ADR 0002 estuvo en Propuesta, `AGENTS.md` prohibía agregar estilos, así que las pantallas de EM-010, EM-033, EM-036, EM-041, EM-060, EM-061, EM-062, EM-070 y EM-071 se hicieron en **HTML semántico sin clases**.
- El 2026-11-04 el equipo aceptó el ADR 0002 (`docs/decisiones/0002-estilos-frontend.md`): Tailwind CSS v4 con `django-tailwind-cli`, la identidad de `DESIGN.md` y las fuentes servidas desde `static/fonts/`.
- **EM-004** ([#95](https://github.com/Alexis01000011/EngiMods/pull/95)) agregó `base.html` (barra, mensajes, pie) y estilos base para el HTML sin clases. Por eso las pantallas viejas se leen bien, pero **no tienen la forma que pide `DESIGN.md`**: ni el sello "Probado", ni el temario lateral con avance, ni las tarjetas, chips, botones píldora ni la ficha de la lección.
- **EM-040** ([#96](https://github.com/Alexis01000011/EngiMods/pull/96), la landing) es la primera pantalla hecha con `DESIGN.md` desde el principio. Úsala como ejemplo de cómo se escriben las clases: `templates/core/home.html`.

El objetivo es que todas las pantallas se vean como una sola aplicación antes de la entrega de semestre (alrededor del 1 de diciembre de 2026).

## Pantallas que se deben actualizar

| Plantilla | Historia de origen | Anatomía en `.claude/skills/disenar-pantalla/pantallas.md` |
|---|---|---|
| `templates/courses/lesson_detail.html` | EM-061, EM-062, EM-070 | Lección (la canónica: `referencia/leccion.html`) |
| `templates/courses/course_detail.html` | EM-041 | Detalle del curso |
| `templates/enrollments/my_courses.html` | EM-060, EM-062 | Mi panel |
| `templates/submissions/submit.html` | EM-070 | Formularios |
| `templates/submissions/my_submissions.html` | EM-070 | Mi panel (lista) y Formularios |
| `templates/submissions/tutor_queue.html` | EM-071 | Vista del tutor |
| `templates/submissions/tutor_review.html` | EM-071 | Vista del tutor |
| `templates/catalog/game_list.html`, `game_detail.html` | EM-010 | Catálogo de juegos |
| `templates/core/legal_text.html` | EM-033, EM-036 | Textos legales |

## Primer paso: darle una historia en el backlog

Sin ID no hay commits de código: el hook `commit-msg` solo acepta `EM-0XX:`, `Docs:` o `Herramientas:`, y esto no es ninguno de los dos últimos. Antes de tocar plantillas:

1. Usa la skill `cambiar-backlog` para agregar la historia (o varias) a `docs/BACKLOG.md`, con su issue en GitHub. Propuesta de corte, que Alexis confirma:
   - **Pantallas del alumno:** lección, detalle del curso, Mi panel y entregas. Es lo que se ve en la demo; va primero.
   - **Pantallas del tutor:** cola y revisión. Coordina con **EM-072** (revisar con rúbrica, #45), que está libre y también cambia `tutor_review.html`. Si alguien toma EM-072, que esa historia ya haga su pantalla con `DESIGN.md` y quita esa plantilla de la deuda.
   - **Catálogo y textos legales.** Ojo con **EM-012** (página de cada juego, #12), que reescribe `game_detail.html`.
2. Pregúntale a Alexis en qué bloque del recorte entra (lo sugerido es el bloque A, por la demo) y que lo apruebe.
3. Asigna la issue a Alexis y sigue la skill `tomar-historia`.

## Rama

Una rama por historia, desde `main` actualizado, con el nombre de `AGENTS.md`, sección 5: `em-0XX-pantallas-alumno-design`, `em-0XX-pantallas-tutor-design`, etc. (cambia `0XX` por el ID que le dé el backlog). **No uses `ux-ui-estilos-design-md`**: es la rama de la sesión que hizo `DESIGN.md`, ya está mezclada y solo tiene esta nota. Si tu entorno te asigna una rama fija, usa esa y díselo a Alexis en el PR.

## Cómo trabajar

- **Lee primero la skill `disenar-pantalla`** (`.claude/skills/disenar-pantalla/SKILL.md`), `DESIGN.md` completo y `pantallas.md`. Abre `referencia/leccion.html` y `referencia/componentes.html` en el navegador: son la forma canónica.
- **Clases:** cada token de `DESIGN.md` es una clase (`bg-primary`, `text-ink-muted`, `font-serif text-title-lg`, `rounded-lg`, `p-md`, `max-w-reading-max`, `button-primary`). La paleta y la escala de texto propias de Tailwind están borradas: `bg-blue-500` o `text-sm` no generan nada. Sin `style=` en línea.
- **Estilos base que estorban:** `assets/tailwind.css` da márgenes a `main p, ul, li…` y una regla `main li + li`. En listas que son rejillas o chips pon `m-0`, `list-none` y `p-0`, como en `home.html`.
- **Piezas repetidas:** el sello "Probado con", los chips y la tarjeta de curso ya se repiten en la landing, la lección y el curso. Si los vas a usar en tres o más plantillas, conviene un `{% include %}` en `templates/components/`; no hagas más abstracción que esa.
- **Para verlas:** `uv run python manage.py tailwind build` (la primera vez descarga el binario de Tailwind desde GitHub) y `uv run python manage.py runserver`. Revisa 360, 768 y 1280 px, sin desplazamiento horizontal. Para tener datos, crea juegos, cursos, lecciones y pruebas en el shell o en el admin; EM-006 (datos de ejemplo) todavía no existe.
- **Pruebas:** las pruebas actuales revisan textos y permisos; **no deben romperse**. Agrega pruebas solo de lo que cambie en comportamiento o estructura (por ejemplo, que la lección actual tenga `aria-current="page"` o que salga el sello correcto).

## Lo que NO debes hacer

- **No inventes datos.** Algunas piezas de `DESIGN.md` piden datos que los modelos no tienen:
  - "Al terminar podrás" (logros de la lección o del curso);
  - quién escribió y revisó la lección, y cuándo;
  - el nombre del tutor.
  
  No los pongas con texto fijo. Deja fuera la pieza o pregúntale a Alexis si se agregan campos; eso sería un cambio de modelo con migración, y conviene que sea una historia aparte.
- **No cambies comportamiento:** permisos, vistas, URLs y reglas de acceso se quedan igual. Esta tarea solo cambia cómo se ve.
- **No toques `DESIGN.md`, `assets/tailwind.css` ni la referencia** salvo que falte un token. Si falta, agrégalo en los tres lugares a la vez; `core/tests/test_design_tokens.py` y `.claude/skills/disenar-pantalla/revisar_tokens.py` revisan que coincidan.
- **No mezcles los PR por tu cuenta.** Abre el PR y detente; Alexis decide.

## Cosas que conviene saber

- Hay lienzos de diseño con las exploraciones y la síntesis en https://claude.ai/artifact/UbxUZFLSyoRtt9VHaFVbde (privado de Alexis; si tu sesión es de su cuenta, puedes leerlo). La página "Síntesis A + B + C" es la que se eligió; lo que manda es `DESIGN.md`.
- La CI de GitHub tuvo colas largas el 2026-11-04. Si el PR se queda "en cola", no es tu código.
- Inicio de sesión (EM-031) todavía no existe: las vistas con `login_required` redirigen a una URL que da 404. En pruebas usa `client.force_login`; para ver pantallas con sesión en el navegador entra por `/admin/` con un superusuario.
