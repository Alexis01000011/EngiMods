# Despliegue a staging

Cómo se despliega, se actualiza, se respalda y se restaura el entorno de staging (EM-005). La elección de proveedores y sus límites están en el ADR 0003 (`docs/decisiones/0003-hosting-staging.md`).

| Pieza | Proveedor y plan | Región |
|---|---|---|
| Web (Django con gunicorn y WhiteNoise) | Render, plan gratuito | Ohio |
| PostgreSQL | Neon, plan gratuito | AWS US East 2 (Ohio) |

La configuración del servicio web está en `render.yaml` (Blueprint de Render) y el build en `scripts/render-build.sh`.

## Reglas

- **Los secretos viven solo en el Dashboard de Render** (y la cadena de conexión, también en Neon). Nunca en el repo, en issues, en PR, en capturas ni en Discord. Esto incluye `DATABASE_URL`: trae la contraseña de la base.
- Una persona administra las cuentas de Render y Neon (ADR 0003). Si alguien más necesita acceso, se le invita como miembro; no se comparten contraseñas.
- En staging solo se usan llaves de Stripe de prueba (`docs/stripe.md`).
- Los respaldos (`*.dump`) tienen datos de personas: se guardan fuera del repo y se borran cuando ya no sirven.

## 1. Crear la base en Neon (una vez)

1. En [neon.com](https://neon.com), crea un proyecto `engimods-staging` con PostgreSQL 17 en la región **AWS US East 2 (Ohio)**. Si Neon pregunta para qué es, elige solo la cadena de conexión (*I just need a database connection string*), no el backend completo. No hace falta el CLI de Neon ni `neon init`: escribiría la cadena en tu `.env` local y tu copia de desarrollo apuntaría a staging.
2. En **Connect**, desactiva *Connection pooling* y copia la cadena de conexión directa (`postgresql://…?sslmode=require`). Es la que usan Django y `pg_dump`. La conexión con *pooling* pasa por PgBouncer y obliga a cambiar cómo Django usa los cursores; para staging no hace falta.
3. Revisa que la suspensión por inactividad (*scale to zero*) esté activa, para no gastar las horas de cómputo del plan gratuito (ADR 0003).

## 2. Crear el servicio en Render (una vez)

1. En [render.com](https://render.com), entra con GitHub y dale acceso al repositorio.
2. **New → Blueprint**, elige el repositorio y la rama `main`. Render lee `render.yaml` y propone el servicio `engimods-staging`. Si alguna vez se crea desde otra rama (por ejemplo, para probar antes de mezclar), se cambia después en **Settings → Build → Source** del servicio.
3. Render pide los valores marcados como secretos en `render.yaml`:
   - `DATABASE_URL`: la cadena directa de Neon del paso 1.
   - `STRIPE_SECRET_KEY` y `STRIPE_PUBLISHABLE_KEY`: las llaves de prueba (`docs/stripe.md`).
   - `STRIPE_WEBHOOK_SECRET`: déjalo vacío hasta registrar el webhook (EM-043, `docs/stripe.md`).
4. Aplica el Blueprint. El primer build tarda unos minutos: instala dependencias con uv, compila Tailwind, corre `collectstatic` y aplica las migraciones en Neon.
5. Abre la URL que muestra Render (`https://engimods-staging….onrender.com`) y `…/health/`, que debe responder `{"status": "ok"}`.

`SECRET_KEY` la genera Render. El dominio del servicio se agrega solo a `ALLOWED_HOSTS` mediante la variable `RENDER_EXTERNAL_HOSTNAME`, que pone Render.

## 3. Primer acceso: superusuario y datos

El plan gratuito de Render no tiene consola, pero la base vive en Neon, así que los comandos de administración se corren desde tu computadora apuntando a ella. La variable va solo en ese comando; no la guardes en `.env`, para no tocar staging por accidente.

```bash
DATABASE_URL='<cadena directa de Neon>' uv run python manage.py createsuperuser
```

Después entra a `/admin/` en staging y captura los juegos, cursos y textos legales que correspondan. No cargues textos legales inventados (`AGENTS.md`, sección 2).

## 4. Desplegar cambios

- Cada mezcla a `main` despliega sola: Render corre `scripts/render-build.sh` y luego arranca gunicorn. Las migraciones se aplican en el build, porque el plan gratuito no tiene paso previo al despliegue.
- Para repetir un despliegue sin cambios: **Manual Deploy → Deploy latest commit** en el servicio.
- Si el build falla, el servicio sigue con la versión anterior. Los errores están en **Logs** del servicio.
- Los errores de Django (500) y los avisos de la app salen en los mismos logs.

## 5. Variables de entorno

| Variable | Valor en staging | Dónde se define |
|---|---|---|
| `DEBUG` | `False` | `render.yaml` |
| `HTTPS_ONLY` | `True`: redirige a HTTPS, cookies seguras y HSTS | `render.yaml` |
| `SECRET_KEY` | aleatoria | Render la genera (`render.yaml`) |
| `WEB_CONCURRENCY` | `2` procesos de gunicorn | `render.yaml` |
| `UV_PYTHON_DOWNLOADS` | `never`: uv usa el Python de Render | `render.yaml` |
| `DATABASE_URL` | cadena directa de Neon | Dashboard de Render |
| `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` | llaves de prueba | Dashboard de Render |
| `RENDER_EXTERNAL_HOSTNAME`, `PORT` | las pone Render | Render |

Las demás variables de `.env.example` usan su valor por defecto. Hasta EM-008 el correo sale por la consola: los enlaces de verificación de cuenta y de recuperación de contraseña aparecen en los logs de Render.

## 6. Respaldo y restauración

Se necesita `pg_dump` y `pg_restore` de la versión 17 o mayor (en Arch, paquete `postgresql-libs`; en Windows, el instalador de PostgreSQL con solo las herramientas de cliente).

**Respaldar**, desde tu computadora:

```bash
pg_dump '<cadena directa de Neon>' --format=custom --no-owner --no-acl \
  --file=engimods-staging-$(date +%F).dump
```

Guarda el archivo fuera del repositorio.

**Restaurar** en una base vacía (por ejemplo, una base nueva en el mismo proyecto de Neon, o un proyecto nuevo si se perdió el original):

```bash
pg_restore --dbname='<cadena de la base vacía>' --no-owner --no-acl engimods-staging-AAAA-MM-DD.dump
```

Para que staging use la base restaurada, cambia `DATABASE_URL` en Render y despliega de nuevo. Para restaurar encima de la base actual, agrega `--clean --if-exists`; borra lo que haya.

Neon también guarda un historial corto de la base para volver a un momento anterior. Su duración en el plan gratuito está sin verificar (ADR 0003), así que no sustituye al respaldo con `pg_dump`.

**Prueba de restauración:** pendiente; se anota aquí con fecha y resultado.

## 7. Comprobaciones

- `manage.py check --deploy` con la configuración de staging no da advertencias; lo cubre `core/tests/test_deploy_settings.py`. Se silencia `security.W021` (precarga de HSTS) porque la lista de precarga no admite subdominios de `onrender.com`.
- `/health/` responde por http sin redirigir. Es el chequeo de salud de Render (`healthCheckPath` en `render.yaml`): si un despliegue nuevo no responde ahí, Render lo cancela y deja la versión anterior.
- Python sale de `.python-version` (3.12; Render usa el último parche). Sin ese archivo Render usaría su versión por defecto, más nueva. Render instala uv porque el repo tiene `uv.lock`, y le pasa a gunicorn el puerto con `GUNICORN_CMD_ARGS`.

## 8. Límites del plan gratuito

- La web se suspende tras 15 minutos sin tráfico y la primera visita tarda en despertarla. Antes de una demostración, abre el sitio unos minutos antes.
- El disco de la web es efímero: nada se guarda ahí. La base está en Neon y las entregas son enlaces a repositorios.
- Neon suspende la base sin tráfico y la primera consulta la despierta.
- Si el piloto recibe alumnos o dinero reales, la web pasa a un plan pagado de Render sin cambiar código (ADR 0003).
