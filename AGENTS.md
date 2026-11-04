# AGENTS.md

Instrucciones para cualquier agente de código (Claude Code, Codex u otro) y para cualquier persona que llegue a este repositorio. Léelo completo antes de tocar código. Con este archivo debes poder empezar a trabajar sin más contexto; los detalles largos están en `docs/`.

> **Pendiente urgente (3/11/2026).** A la issue de EM-020 (#15) le falta la etiqueta `decision-pendiente`. Siguen abiertos el juego de Misión Cero y cuántos días dura el acceso, y EM-020 está en la ruta crítica del recorte de semestre. Quien lea esto primero pone la etiqueta (`gh issue edit 15 --add-label decision-pendiente`) y borra este aviso en un PR `Docs:`. Si eres un agente, díselo a tu humano al inicio de la sesión y ofrécete a hacerlo.

## 1. Qué es EngiMods

Academia en línea, en español, para aprender a **crear mods de videojuegos aplicando ingeniería de software**: arquitectura, Git, pruebas, calidad, documentación, publicación y mantenimiento. No es un curso para copiar código: el alumno construye su propio mod y un tutor revisa lo que entrega.

- **Multi-juego.** El proyecto empezó enfocado en Hytale y se pivoteó a mods de videojuegos en general. La plataforma modela juegos, versiones del juego y entornos de modding (loaders, SDK, herramientas) como datos. Nunca escribas lógica pensando en un juego concreto.
- **Diferenciador clave:** cada lección y recurso dice con qué versión del juego y del entorno fue probado, y se marca como pendiente de revalidar cuando sale una versión nueva.
- **Oferta:** *Misión Cero* (práctica corta, precio de entrada) y luego un *curso de seis semanas* por grupos de hasta 8 alumnos, con revisión de entregas en 24 horas, clínicas grupales y comunidad en Discord. Cobro con Stripe.
- **Público inicial:** hispanohablantes, principalmente en México, con computadora, el juego y programación básica.
- **Origen:** proyecto del Equipo 8 de la materia Negocios Electrónicos (Ingeniería de Software, Universidad Autónoma de Zacatecas), con intención de operarlo de verdad. Nada se diseña solo para entregar.

Los precios, cupos y plazos son **hipótesis a validar en un piloto**, no datos. Contexto completo en `docs/negocio.md`.

## 2. Estado actual (noviembre 2026)

- Hechas: EM-001 (base Django) y EM-002 (CI).
- Solo existe la app `core` (inicio provisional y `/health/`). No hay modelos ni migraciones propias todavía.
- **Lo siguiente es EM-003 (modelo de usuario personalizado).** Hasta que esté en `main`, no crees modelos con relación al usuario ni migraciones en otras apps. Si corriste `migrate` antes de EM-003, borra tu `db.sqlite3` local después de que se mezcle.
- **Hay un recorte vigente para la entrega de semestre** (hasta alrededor del 1 de diciembre de 2026). El objetivo es Misión Cero de punta a punta en staging. Solo se toman historias de ese recorte; ver la sección "Recorte para la entrega de semestre" en `docs/BACKLOG.md`.
- Decidido: Misión Cero es autoguiada (sin grupo), el acceso al contenido es por tiempo y el tutor trabaja en pantallas propias, no en el admin. Ver `docs/arquitectura.md`.
- Decisiones abiertas que no debes inventar: hosting, proveedor de correo, enfoque de estilos (Tailwind u otro), juegos con los que arranca el piloto, días de acceso, textos legales. Ver la sección final de `docs/BACKLOG.md`.

## 3. Stack y comandos

- Python 3.12+, **Django 5.2 LTS**, gestionado con **uv** (`pyproject.toml` + `uv.lock`).
- `django-environ` para configuración; SQLite en desarrollo, PostgreSQL en producción vía `DATABASE_URL`.
- Plantillas de Django renderizadas en el servidor. Sin frontend separado.
- Pruebas con `pytest` + `pytest-django`. Lint y formato con `ruff`.
- CI en GitHub Actions (`.github/workflows/ci.yml`).

```bash
uv sync                                   # instala dependencias (crea .venv)
cp .env.example .env                      # solo la primera vez
uv run python manage.py migrate
uv run python manage.py runserver

uv run pytest                             # pruebas
uv run ruff check . --fix                 # lint
uv run ruff format .                      # formato
uv run python manage.py makemigrations --check --dry-run   # que no falten migraciones
```

Antes de abrir un PR deben pasar los cuatro comandos de la CI: `ruff check .`, `ruff format --check .`, `makemigrations --check --dry-run` y `pytest`. Si tocaste `docs/BACKLOG.md`, también `uv run python scripts/backlog.py`.

Para agregar una dependencia: `uv add <paquete>` (o `uv add --dev <paquete>`). Justifícala en el PR. No edites `uv.lock` a mano.

## 4. Estructura del repositorio

```
AGENTS.md            este archivo (fuente de verdad para agentes)
CLAUDE.md            importa este archivo para Claude Code
README.md            arranque rápido para personas
config/              settings.py, urls.py, wsgi/asgi
core/                app base (inicio, health, utilidades compartidas)
templates/           plantillas globales (base.html) y por app (templates/<app>/)
static/              archivos estáticos globales
docs/
  BACKLOG.md         product backlog completo: historias, criterios, prioridad, dependencias
  arquitectura.md    mapa de apps, modelos previstos y reglas del modelo de datos
  negocio.md         contexto de negocio, oferta e hipótesis
  flujo-de-trabajo.md  sprints, etiquetas, Definition of Ready, refinamiento
  decisiones/        registros de decisiones (ADR) numerados
scripts/             backlog.py (chequeo del backlog) y agent_hook.py (hooks de agente)
.githooks/           git hooks del repo (sección 10)
.claude/             skills y hooks de Claude Code
.codex/              hooks de Codex
.agents/skills/      enlaces a las skills para Codex
.github/             CI, plantillas de issues y de PR
```

Apps previstas y de qué es dueña cada una: `core`, `accounts`, `catalog`, `courses`, `cohorts`, `enrollments`, `payments`, `submissions`, `metrics`. La tabla completa está en `docs/arquitectura.md`. Crea una app solo cuando llegue la historia que la necesita, con `uv run python manage.py startapp <nombre>` en la raíz, y regístrala en `INSTALLED_APPS`.

## 5. Cómo tomar y entregar trabajo

Cada historia tiene un ID `EM-###`, una sección en `docs/BACKLOG.md` y una GitHub Issue con el mismo ID en el título.

1. **Elige una historia** de la ola más baja disponible cuyas dependencias estén cerradas. Mientras esté vigente el recorte de semestre, toma solo del bloque A, después del B y después del C (sección "Recorte para la entrega de semestre" en `docs/BACKLOG.md`). Fuera del recorte, usa la sección "Orden sugerido" y prioriza `Must` sobre `Should` y `Could`. No tomes nada de R2 (post-piloto).
2. **Verifica que nadie la tenga:** `gh issue list --search "EM-0XX in:title"` y `gh issue view <número>`. Si está asignada a otra persona, elige otra. Si no tienes `gh`, pregúntale a tu humano.
3. **Asígnala** a la persona para la que trabajas (`gh issue edit <número> --add-assignee @me`) antes de escribir código. Una persona (y su agente) trabaja en una historia a la vez.
4. **Rama** desde `main` actualizado: `em-0XX-descripcion-corta` (por ejemplo `em-043-webhook-stripe`).
5. **Implementa solo esa historia**, cumpliendo todos sus criterios de aceptación. Si descubres trabajo extra, no lo metas: propón una historia nueva en el PR.
6. **Commits** en español, en imperativo y con el ID: `EM-043: verifica la firma del webhook`. Lo que no es de una historia empieza con `Docs:` (documentación) o `Herramientas:` (CI, hooks, skills, scripts).
7. **PR** con título `EM-0XX: <título de la historia>`, `Closes #<número>` en la descripción y la plantilla de PR llena (criterios marcados uno por uno). Otra persona del equipo revisa y aprueba. Se mezcla con *squash*.
8. Si el alcance o los criterios cambian, actualiza la sección de la historia en `docs/BACKLOG.md` **en el mismo PR**.

## 6. Convenciones de código

- **Idioma:** identificadores de código en inglés (modelos, funciones, variables). Todo lo que ve el usuario (plantillas, mensajes, correos, `verbose_name`) en español de México. Envuelve los textos visibles con `gettext_lazy as _` para no cerrar la puerta a otro idioma.
- **Modelos:** `TextChoices` para estados; dinero en centavos enteros MXN; `settings.AUTH_USER_MODEL` para referirse al usuario; `__str__` en cada modelo; registrar en el admin con `list_display` y filtros útiles.
- **Datos de negocio como datos:** precios, cupos, plazos, enlaces de Discord y textos legales se capturan en la base de datos o en settings, nunca como constantes en código.
- **Vistas:** vistas basadas en funciones o clases, lo que sea más simple. Protege con `login_required` y verifica permisos (inscrito, tutor del grupo) en cada vista que muestre contenido de pago.
- **URLs** públicas en español (`/juegos/`, `/cursos/`, `/mi-panel/`), con `app_name` y `reverse()`.
- **Plantillas** en `templates/<app>/` extendiendo `base.html`.
- **Pruebas** en `<app>/tests/test_*.py`. Cada criterio de aceptación que sea comportamiento debe tener al menos una prueba. Prueba permisos (quién no debe ver algo).
- **Migraciones:** solo en las apps que toca tu historia. Nunca edites una migración que ya está en `main`. Si al actualizar tu rama hay conflicto de migraciones, borra tus migraciones no mezcladas y vuelve a generarlas.
- **Seguridad:** el contenido Markdown se sanitiza al renderizar; webhooks verifican firma; nunca registres llaves ni datos de pago en logs.
- Mantén las cosas simples. Nada de capas, abstracciones o dependencias que la historia no pida.

## 7. Definition of Done

Una historia está terminada cuando:

- [ ] Cumple todos sus criterios de aceptación de `docs/BACKLOG.md`.
- [ ] Tiene pruebas para el comportamiento nuevo, incluidos los casos de permisos.
- [ ] Pasa la CI: `ruff check`, `ruff format --check`, `makemigrations --check` y `pytest`.
- [ ] Las pantallas nuevas están en español y se ven bien en teléfono.
- [ ] No hay secretos, llaves ni datos personales reales en el código, fixtures o commits.
- [ ] Si agregó variables de entorno, están en `.env.example` con comentario.
- [ ] Si tomó una decisión de arquitectura o de proveedor, hay un ADR en `docs/decisiones/`.
- [ ] Otra persona del equipo revisó y aprobó el PR.

## 8. Lo que un agente no debe hacer

- No inventes reglas de negocio, precios, políticas de devolución, textos legales ni datos de costos. Si una historia necesita uno de estos datos y no está definido, déjalo configurable y pregúntale a tu humano. En el PR, marca qué quedó como supuesto.
- No elijas proveedores (hosting, correo, almacenamiento) ni el enfoque de estilos por tu cuenta: proponlo con un ADR y que el equipo decida.
- No trabajes en más de una historia por PR ni hagas refactors no pedidos en código de otras historias.
- No hagas push directo a `main`, no fuerces push sobre ramas ajenas y no mezcles tus propios PR sin revisión.
- No subas `.env`, `db.sqlite3`, `media/` ni llaves de Stripe (aunque sean de prueba).
- No escribas lógica específica de un juego.

## 9. Dónde buscar

| Necesitas | Ve a |
|---|---|
| Qué construir, criterios y dependencias | `docs/BACKLOG.md` |
| Quién está trabajando en qué | GitHub Issues (asignado, abiertas o cerradas) |
| Qué app es dueña de qué modelo | `docs/arquitectura.md` |
| Por qué existe el producto y qué debe validar | `docs/negocio.md` |
| Sprints, etiquetas, Definition of Ready | `docs/flujo-de-trabajo.md` |
| Por qué se decidió algo técnico | `docs/decisiones/` |

## 10. Skills y hooks

El repo trae skills y hooks que funcionan igual en Claude Code y en Codex.

**Skills.** En Claude Code se invocan con `/nombre` y en Codex con `$nombre`. También se activan solas cuando la petición encaja.

| Skill | Para qué |
|---|---|
| `tomar-historia` | Elegir, reclamar, implementar y entregar una historia (sección 5) |
| `revisar-pr` | Revisar un PR contra sus criterios, la Definition of Done y las reglas |
| `cambiar-backlog` | Cambiar `docs/BACKLOG.md` sin desincronizar índice, olas, recorte e issues |
| `proponer-adr` | Preparar una decisión técnica o de proveedor para que el equipo la tome |

Cada skill vive en `.claude/skills/<nombre>/` (archivos normales, para que funcione en Windows). `.agents/skills/<nombre>` es un enlace simbólico para Codex. Para agregar una, crea su carpeta y el enlace: `ln -s ../../.claude/skills/<nombre> .agents/skills/<nombre>`. La CI revisa que el enlace exista.

**Hooks**, en dos capas:

- **Git hooks** (`.githooks/`), para personas y agentes:
  - Bloquean el commit y el push a `main`.
  - Bloquean subir `.env`, `db.sqlite3`, `media/` o llaves de Stripe.
  - Corren ruff antes del commit y el chequeo de migraciones antes del push. Las pruebas solo corren en la CI.
  - Exigen el formato del mensaje de commit (sección 5).
- **Hooks de agente** (`scripts/agent_hook.py`, conectados en `.claude/settings.json` y `.codex/hooks.json`):
  - Bloquean `--no-verify`, desactivar los git hooks, `git push --force` (sí permiten `--force-with-lease`), el push a `main` y `gh pr merge`.
  - Bloquean editar `uv.lock`, `.env` y migraciones que ya están en `main`.
  - Al iniciar sesión le dan al agente la rama, su historia y avisos de configuración.

Si un hook te bloquea, corrige la causa; no lo rodees. Si crees que el hook está mal, díselo a tu humano.

**Activación, una vez por persona y por copia del repo.** Las skills llegan solas con `git pull`; los hooks no:

1. `git config core.hooksPath .githooks`
2. Tener `uv` instalado. Lo usan los git hooks y, en Claude Code, los hooks de agente.
3. En Codex: abrir `/hooks` y aprobar los hooks del proyecto. Codex vuelve a pedir la aprobación cada vez que cambian.
4. En Claude Code no hace falta nada más: los hooks cargan al confiar en la carpeta del proyecto. En Windows necesita Git Bash, que viene con Git for Windows.

**Recordatorio para agentes:** al iniciar sesión debes recibir un bloque que empieza con `[EngiMods] Contexto de la sesión`. Si no llegó, o trae un AVISO, los hooks de esta copia no están completos. Díselo a tu humano una sola vez, al principio, con los pasos de arriba, y recuérdale avisar a quien del equipo no lo haya hecho. Luego sigue con lo que te pidió.
