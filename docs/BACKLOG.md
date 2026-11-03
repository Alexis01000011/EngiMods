# Product backlog de EngiMods

Catálogo completo de lo que se va a construir en la plataforma. Generado el 3 de noviembre de 2026 a partir del lienzo de modelo de negocio (28/09/2026), el documento de hipótesis y pitch, y el pivote a mods de videojuegos en general.

## Cómo leer este documento

- **Este archivo define el alcance.** Las GitHub Issues llevan el estado (quién la tiene, si está abierta o cerrada). Si cambia el alcance o los criterios de una historia, se cambia aquí en un PR y se actualiza la issue.
- **ID:** `EM-###`. La decena indica la épica (EM-04x es Landing y venta). Es el mismo ID en la issue, la rama y el PR.
- **Prioridad (MoSCoW) dentro del release R1 (piloto):** `Must` sin esto no hay piloto; `Should` importante pero el piloto puede correr sin ello; `Could` solo si sobra tiempo. `Later` es post-piloto (R2).
- **Puntos:** estimación inicial de complejidad relativa (1, 2, 3, 5, 8). Son una propuesta para arrancar, no una medición; el equipo las ajusta en refinamiento.
- **Ola:** orden sugerido según dependencias. Todo lo de una misma ola se puede trabajar en paralelo cuando la ola anterior está lista. Ola 0 es lo que ya está hecho.
- **Fuera de este backlog:** la creación del contenido de los cursos (escribir y probar lecciones para cada juego) es trabajo del equipo de contenido, no de la plataforma.

## Resumen por épica

| Épica | Nombre | Historias R1 | Puntos R1 (Must) | Puntos R1 (total) | Historias R2 |
|---|---|---|---|---|---|
| E0 | Fundaciones técnicas | 9 | 18 | 23 | 0 |
| E1 | Catálogo de juegos y versiones | 5 | 8 | 15 | 0 |
| E2 | Cursos y contenido | 5 | 12 | 15 | 0 |
| E3 | Cuentas y datos personales | 5 | 9 | 14 | 0 |
| E4 | Landing y venta | 10 | 21 | 31 | 0 |
| E5 | Grupos (cohortes) | 4 | 5 | 10 | 0 |
| E6 | Experiencia de aprendizaje | 4 | 8 | 11 | 0 |
| E7 | Entregas y revisión | 7 | 13 | 21 | 0 |
| E8 | Comunidad y comunicación | 3 | 1 | 7 | 0 |
| E9 | Operación y métricas del piloto | 4 | 5 | 9 | 0 |
| E10 | Post-piloto | 0 | 0 | 0 | 9 |
| | **Total** | **56** | **100** | **156** | **9** |

## Orden sugerido para R1 (olas por dependencias)

**Ola 0 (hecho):** [EM-001](#em-001) Base del proyecto Django (Must), [EM-002](#em-002) Integración continua en GitHub Actions (Must)

**Ola 1:** [EM-003](#em-003) Modelo de usuario personalizado (Must), [EM-004](#em-004) Plantilla base y sistema de estilos (Must), [EM-005](#em-005) Despliegue a un entorno de pruebas (staging) (Must), [EM-009](#em-009) Cuenta de Stripe en modo prueba conectada (Must)

**Ola 2:** [EM-007](#em-007) Almacenamiento de archivos subidos (Could), [EM-008](#em-008) Correo transaccional en producción (Must), [EM-010](#em-010) Registrar juegos en el catálogo (Must), [EM-033](#em-033) Aviso de privacidad y consentimiento (Must)

**Ola 3:** [EM-011](#em-011) Registrar versiones del juego y entornos de modding (Must), [EM-020](#em-020) Modelo de curso (Must), [EM-030](#em-030) Registro con correo y verificación (Must), [EM-046](#em-046) Lista de espera e interés por juego (Should)

**Ola 4:** [EM-012](#em-012) Página pública de cada juego (Must), [EM-021](#em-021) Módulos y lecciones con versión probada (Must), [EM-031](#em-031) Inicio de sesión, cierre y recuperación de contraseña (Must), [EM-032](#em-032) Perfil del alumno (Should), [EM-050](#em-050) Crear grupos de un curso (Must)

**Ola 5:** [EM-006](#em-006) Datos de ejemplo para desarrollo (Should), [EM-013](#em-013) Filtrar cursos por juego (Should), [EM-014](#em-014) Marcar contenido pendiente de revalidar al salir una nueva versión (Should), [EM-023](#em-023) Recursos descargables y plantillas por lección (Must), [EM-024](#em-024) Lección de muestra gratuita (Must), [EM-034](#em-034) Solicitar baja de la cuenta y de los datos (Could), [EM-040](#em-040) Landing de EngiMods (Must), [EM-042](#em-042) Pago con Stripe Checkout (Must), [EM-053](#em-053) Inscripciones e inscripción manual por administrador (Must), [EM-081](#em-081) Avisos del curso (Should)

**Ola 6:** [EM-041](#em-041) Página de detalle del curso (Must), [EM-043](#em-043) Webhook de Stripe que confirma el pago e inscribe (Must), [EM-045](#em-045) Cupo máximo por grupo (Must), [EM-049](#em-049) Códigos de descuento (Could), [EM-060](#em-060) Panel del alumno: mis cursos (Must), [EM-082](#em-082) Aviso de nueva versión del juego a alumnos afectados (Could)

**Ola 7:** [EM-044](#em-044) Correo de confirmación de compra (Must), [EM-047](#em-047) Registrar devoluciones (Should), [EM-048](#em-048) Pago en efectivo en OXXO (Could), [EM-052](#em-052) Calendario de clínicas grupales (Should), [EM-061](#em-061) Ver una lección (Must), [EM-063](#em-063) Guía de laboratorio local por juego (Should), [EM-080](#em-080) Acceso al Discord del grupo (Must), [EM-093](#em-093) Encuesta de cierre del curso (Should)

**Ola 8:** [EM-022](#em-022) Vista previa de lecciones para tutores (Should), [EM-051](#em-051) Liberar contenido por semana (Should), [EM-062](#em-062) Marcar lección como completada (Must), [EM-070](#em-070) Enviar una entrega (Must)

**Ola 9:** [EM-071](#em-071) Cola de revisión con alerta de 24 horas (Must), [EM-075](#em-075) Entregar archivo .zip (Could), [EM-090](#em-090) Admin configurado para operar el piloto (Must)

**Ola 10:** [EM-072](#em-072) Revisar con rúbrica (Must), [EM-092](#em-092) Exportar datos operativos a CSV (Should)

**Ola 11:** [EM-073](#em-073) Reenviar entrega tras cambios (Must), [EM-074](#em-074) Notificaciones de entregas por correo (Should), [EM-076](#em-076) Proyecto final con checklist de publicación (Should), [EM-091](#em-091) Métricas del piloto (Must)

## Índice

| ID | Título | Épica | Prioridad | Pts | Ola | Depende de | Estado |
|---|---|---|---|---|---|---|---|
| [EM-001](#em-001) | Base del proyecto Django | E0 | Must | 2 | 0 | - | Hecho |
| [EM-002](#em-002) | Integración continua en GitHub Actions | E0 | Must | 1 | 0 | EM-001 | Hecho |
| [EM-003](#em-003) | Modelo de usuario personalizado | E0 | Must | 2 | 1 | EM-001 | Pendiente |
| [EM-004](#em-004) | Plantilla base y sistema de estilos | E0 | Must | 3 | 1 | EM-001 | Pendiente |
| [EM-005](#em-005) | Despliegue a un entorno de pruebas (staging) | E0 | Must | 5 | 1 | EM-001 | Pendiente |
| [EM-006](#em-006) | Datos de ejemplo para desarrollo | E0 | Should | 2 | 5 | EM-003, EM-011, EM-021, EM-050 | Pendiente |
| [EM-007](#em-007) | Almacenamiento de archivos subidos | E0 | Could | 3 | 2 | EM-005 | Pendiente |
| [EM-008](#em-008) | Correo transaccional en producción | E0 | Must | 3 | 2 | EM-005 | Pendiente |
| [EM-009](#em-009) | Cuenta de Stripe en modo prueba conectada | E0 | Must | 2 | 1 | EM-001 | Pendiente |
| [EM-010](#em-010) | Registrar juegos en el catálogo | E1 | Must | 2 | 2 | EM-003 | Pendiente |
| [EM-011](#em-011) | Registrar versiones del juego y entornos de modding | E1 | Must | 3 | 3 | EM-010 | Pendiente |
| [EM-012](#em-012) | Página pública de cada juego | E1 | Must | 3 | 4 | EM-011, EM-020 | Pendiente |
| [EM-013](#em-013) | Filtrar cursos por juego | E1 | Should | 2 | 5 | EM-012 | Pendiente |
| [EM-014](#em-014) | Marcar contenido pendiente de revalidar al salir una nueva versión | E1 | Should | 5 | 5 | EM-021 | Pendiente |
| [EM-020](#em-020) | Modelo de curso | E2 | Must | 3 | 3 | EM-010 | Pendiente |
| [EM-021](#em-021) | Módulos y lecciones con versión probada | E2 | Must | 5 | 4 | EM-020, EM-011 | Pendiente |
| [EM-022](#em-022) | Vista previa de lecciones para tutores | E2 | Should | 3 | 8 | EM-021, EM-061 | Pendiente |
| [EM-023](#em-023) | Recursos descargables y plantillas por lección | E2 | Must | 2 | 5 | EM-021 | Pendiente |
| [EM-024](#em-024) | Lección de muestra gratuita | E2 | Must | 2 | 5 | EM-021 | Pendiente |
| [EM-030](#em-030) | Registro con correo y verificación | E3 | Must | 5 | 3 | EM-003, EM-004, EM-033 | Pendiente |
| [EM-031](#em-031) | Inicio de sesión, cierre y recuperación de contraseña | E3 | Must | 2 | 4 | EM-030 | Pendiente |
| [EM-032](#em-032) | Perfil del alumno | E3 | Should | 2 | 4 | EM-030, EM-010 | Pendiente |
| [EM-033](#em-033) | Aviso de privacidad y consentimiento | E3 | Must | 2 | 2 | EM-003 | Pendiente |
| [EM-034](#em-034) | Solicitar baja de la cuenta y de los datos | E3 | Could | 3 | 5 | EM-032 | Pendiente |
| [EM-040](#em-040) | Landing de EngiMods | E4 | Must | 3 | 5 | EM-004, EM-012 | Pendiente |
| [EM-041](#em-041) | Página de detalle del curso | E4 | Must | 3 | 6 | EM-020, EM-024, EM-050 | Pendiente |
| [EM-042](#em-042) | Pago con Stripe Checkout | E4 | Must | 5 | 5 | EM-009, EM-030, EM-050 | Pendiente |
| [EM-043](#em-043) | Webhook de Stripe que confirma el pago e inscribe | E4 | Must | 5 | 6 | EM-042, EM-053 | Pendiente |
| [EM-044](#em-044) | Correo de confirmación de compra | E4 | Must | 2 | 7 | EM-043, EM-008 | Pendiente |
| [EM-045](#em-045) | Cupo máximo por grupo | E4 | Must | 3 | 6 | EM-042 | Pendiente |
| [EM-046](#em-046) | Lista de espera e interés por juego | E4 | Should | 2 | 3 | EM-010, EM-033 | Pendiente |
| [EM-047](#em-047) | Registrar devoluciones | E4 | Should | 3 | 7 | EM-043 | Pendiente |
| [EM-048](#em-048) | Pago en efectivo en OXXO | E4 | Could | 3 | 7 | EM-043, EM-045 | Pendiente |
| [EM-049](#em-049) | Códigos de descuento | E4 | Could | 2 | 6 | EM-042 | Pendiente |
| [EM-050](#em-050) | Crear grupos de un curso | E5 | Must | 3 | 4 | EM-020, EM-003 | Pendiente |
| [EM-051](#em-051) | Liberar contenido por semana | E5 | Should | 3 | 8 | EM-050, EM-061 | Pendiente |
| [EM-052](#em-052) | Calendario de clínicas grupales | E5 | Should | 2 | 7 | EM-050, EM-060 | Pendiente |
| [EM-053](#em-053) | Inscripciones e inscripción manual por administrador | E5 | Must | 2 | 5 | EM-050 | Pendiente |
| [EM-060](#em-060) | Panel del alumno: mis cursos | E6 | Must | 3 | 6 | EM-053 | Pendiente |
| [EM-061](#em-061) | Ver una lección | E6 | Must | 3 | 7 | EM-021, EM-060 | Pendiente |
| [EM-062](#em-062) | Marcar lección como completada | E6 | Must | 2 | 8 | EM-061 | Pendiente |
| [EM-063](#em-063) | Guía de laboratorio local por juego | E6 | Should | 3 | 7 | EM-011, EM-060 | Pendiente |
| [EM-070](#em-070) | Enviar una entrega | E7 | Must | 3 | 8 | EM-061 | Pendiente |
| [EM-071](#em-071) | Cola de revisión con alerta de 24 horas | E7 | Must | 3 | 9 | EM-070 | Pendiente |
| [EM-072](#em-072) | Revisar con rúbrica | E7 | Must | 5 | 10 | EM-071 | Pendiente |
| [EM-073](#em-073) | Reenviar entrega tras cambios | E7 | Must | 2 | 11 | EM-072 | Pendiente |
| [EM-074](#em-074) | Notificaciones de entregas por correo | E7 | Should | 2 | 11 | EM-072, EM-008 | Pendiente |
| [EM-075](#em-075) | Entregar archivo .zip | E7 | Could | 3 | 9 | EM-070, EM-007 | Pendiente |
| [EM-076](#em-076) | Proyecto final con checklist de publicación | E7 | Should | 3 | 11 | EM-072 | Pendiente |
| [EM-080](#em-080) | Acceso al Discord del grupo | E8 | Must | 1 | 7 | EM-050, EM-060 | Pendiente |
| [EM-081](#em-081) | Avisos del curso | E8 | Should | 3 | 5 | EM-050, EM-008 | Pendiente |
| [EM-082](#em-082) | Aviso de nueva versión del juego a alumnos afectados | E8 | Could | 3 | 6 | EM-014, EM-081 | Pendiente |
| [EM-090](#em-090) | Admin configurado para operar el piloto | E9 | Must | 2 | 9 | EM-053, EM-070 | Pendiente |
| [EM-091](#em-091) | Métricas del piloto | E9 | Must | 3 | 11 | EM-062, EM-072 | Pendiente |
| [EM-092](#em-092) | Exportar datos operativos a CSV | E9 | Should | 2 | 10 | EM-090 | Pendiente |
| [EM-093](#em-093) | Encuesta de cierre del curso | E9 | Should | 2 | 7 | EM-060 | Pendiente |
| [EM-100](#em-100) | Membresía de actualizaciones | E10 | Later | - | - | - | Pendiente |
| [EM-101](#em-101) | Talleres para grupos bajo cotización | E10 | Later | - | - | - | Pendiente |
| [EM-102](#em-102) | Ruta introductoria para quienes empiezan de cero | E10 | Later | - | - | - | Pendiente |
| [EM-103](#em-103) | Portafolio público del alumno | E10 | Later | - | - | - | Pendiente |
| [EM-104](#em-104) | Constancia de finalización verificable | E10 | Later | - | - | - | Pendiente |
| [EM-105](#em-105) | Espacio para aliados y creadores | E10 | Later | - | - | - | Pendiente |
| [EM-106](#em-106) | Varios tutores y reparto de revisiones | E10 | Later | - | - | - | Pendiente |
| [EM-107](#em-107) | Facturación electrónica (CFDI) | E10 | Later | - | - | - | Pendiente |
| [EM-108](#em-108) | Plataforma en inglés | E10 | Later | - | - | - | Pendiente |

## Historias

### E0 Fundaciones técnicas

Base del proyecto, infraestructura, despliegue y servicios externos.

#### EM-001

**Base del proyecto Django**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 0 · Estado: Hecho

Criterios de aceptación:

- [x] Proyecto Django 5.2 LTS gestionado con uv (`pyproject.toml` + `uv.lock`).
- [x] Configuración por variables de entorno con `django-environ` y `.env.example`.
- [x] App `core` con página de inicio provisional y `/health/`.
- [x] pytest + pytest-django con pruebas de humo pasando.

#### EM-002

**Integración continua en GitHub Actions**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 1 · Ola: 0 · Estado: Hecho

Criterios de aceptación:

- [x] En cada PR y push a `main` corren: `ruff check`, `ruff format --check`, `makemigrations --check` y `pytest`.
- [x] Un PR con CI en rojo no se mezcla.

Depende de: [EM-001](#em-001)

#### EM-003

**Modelo de usuario personalizado**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 1

Criterios de aceptación:

- [ ] Existe la app `accounts` con `User(AbstractUser)` y `AUTH_USER_MODEL = "accounts.User"`.
- [ ] El correo es único y es el identificador para iniciar sesión.
- [ ] El modelo está registrado en el admin.
- [ ] Es la primera migración del proyecto: ninguna otra app crea migraciones que dependan de `auth.User` antes de esto.

Depende de: [EM-001](#em-001)

Nota: Bloquea casi todo lo demás. Cambiar el modelo de usuario después de tener migraciones es costoso, por eso va primero.

#### EM-004

**Plantilla base y sistema de estilos**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 1

Criterios de aceptación:

- [ ] `templates/base.html` con navegación, pie de página y mensajes de Django.
- [ ] Se decide y documenta en `docs/decisiones/` el enfoque de estilos (por ejemplo Tailwind o CSS propio) con su razón.
- [ ] La plantilla se ve bien en pantalla de teléfono (360 px de ancho) y de escritorio.

Depende de: [EM-001](#em-001)

#### EM-005

**Despliegue a un entorno de pruebas (staging)**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 5 · Ola: 1

Criterios de aceptación:

- [ ] Se elige proveedor de hosting y se documenta en `docs/decisiones/` con su costo mensual consultado en la fuente oficial y la fecha de consulta.
- [ ] Base de datos PostgreSQL, archivos estáticos servidos (por ejemplo con WhiteNoise) y HTTPS.
- [ ] Los secretos viven en variables de entorno del proveedor, nunca en el repo.
- [ ] `DEBUG=False` en staging y `manage.py check --deploy` sin advertencias críticas.
- [ ] El despliegue se puede repetir siguiendo pasos escritos en `docs/despliegue.md`.

Depende de: [EM-001](#em-001)

Nota: Presupuesto del piloto en el lienzo: hasta MXN 1,500. El costo del hosting tiene que caber ahí.

#### EM-006

**Datos de ejemplo para desarrollo**

Tipo: Técnica · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 5

Criterios de aceptación:

- [ ] Comando `python manage.py seed_demo` que crea: 2 juegos con versiones, 1 curso por juego con módulos y lecciones, 1 grupo, 1 tutor y 2 alumnos.
- [ ] Se puede correr varias veces sin duplicar datos.
- [ ] Documentado en el README.

Depende de: [EM-003](#em-003), [EM-011](#em-011), [EM-021](#em-021), [EM-050](#em-050)

Nota: Permite que varias personas (y sus agentes) trabajen en pantallas distintas sin depender de capturar datos a mano.

#### EM-007

**Almacenamiento de archivos subidos**

Tipo: Técnica · Prioridad: Could · Release: R1 · Puntos: 3 · Ola: 2

Criterios de aceptación:

- [ ] En desarrollo los archivos se guardan en `media/`.
- [ ] En producción se usa un almacenamiento compatible con S3 configurado por variables de entorno.
- [ ] Límite de tamaño y tipos de archivo permitidos configurables.

Depende de: [EM-005](#em-005)

Nota: Solo hace falta si se aceptan entregas en .zip (EM-075) o descargables como archivo. Para el piloto se pueden usar enlaces a repos plantilla.

#### EM-008

**Correo transaccional en producción**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 2

Criterios de aceptación:

- [ ] Se elige proveedor de correo y se documenta con costo consultado y fecha.
- [ ] Dominio configurado con SPF y DKIM; los correos de prueba no llegan a spam en Gmail y Outlook.
- [ ] En desarrollo se sigue usando el backend de consola.

Depende de: [EM-005](#em-005)

#### EM-009

**Cuenta de Stripe en modo prueba conectada**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 1

Criterios de aceptación:

- [ ] Llaves de prueba de Stripe leídas de variables de entorno (`STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`).
- [ ] Instrucciones en `docs/stripe.md` para probar webhooks en local con Stripe CLI.
- [ ] Ninguna llave real en el repositorio ni en los logs.

Depende de: [EM-001](#em-001)

### E1 Catálogo de juegos y versiones

Juegos soportados, sus versiones y entornos de modding. Es lo que permite decir con qué versión se probó cada recurso.

#### EM-010

**Registrar juegos en el catálogo**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 2

> Como **administrador**, quiero registrar los juegos para los que EngiMods ofrece contenido, para poder ofrecer cursos de varios juegos desde una sola plataforma.

Criterios de aceptación:

- [ ] Desde el admin puedo crear un juego con nombre, slug, descripción corta, sitio oficial y logo.
- [ ] Un juego tiene estado `activo` u `oculto`; los ocultos no aparecen en páginas públicas.
- [ ] El slug es único y se usa en las URLs públicas.

Depende de: [EM-003](#em-003)

#### EM-011

**Registrar versiones del juego y entornos de modding**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 3

> Como **administrador**, quiero registrar las versiones de cada juego y los entornos de modding que usamos (loader, SDK o herramienta, con su versión), para que cada lección pueda declarar con qué combinación exacta fue probada.

Criterios de aceptación:

- [ ] Una versión del juego tiene número de versión, fecha de publicación y una marca de `versión actual` (solo una por juego).
- [ ] Un entorno de modding pertenece a un juego y tiene nombre y versión (por ejemplo un loader, un SDK oficial o una herramienta de la comunidad).
- [ ] Se puede indicar con qué versiones del juego es compatible cada entorno.
- [ ] Todo se administra desde el admin con filtros por juego.

Depende de: [EM-010](#em-010)

Nota: El modelo debe servir para cualquier juego; no se asume nada específico de un juego en particular.

#### EM-012

**Página pública de cada juego**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 4

> Como **visitante**, quiero ver una página de cada juego con sus cursos disponibles y las versiones que soportamos, para saber si EngiMods me sirve para el juego que me interesa.

Criterios de aceptación:

- [ ] URL `/juegos/<slug>/` con descripción, versión actual soportada y lista de cursos publicados de ese juego.
- [ ] Si el juego no tiene cursos publicados, se indica y, cuando EM-046 esté hecha, se ofrece dejar el correo.
- [ ] Listado general `/juegos/` con todos los juegos activos.

Depende de: [EM-011](#em-011), [EM-020](#em-020)

#### EM-013

**Filtrar cursos por juego**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 5

> Como **visitante**, quiero filtrar el catálogo de cursos por juego y por nivel, para encontrar rápido lo que me sirve.

Criterios de aceptación:

- [ ] El listado de cursos tiene filtro por juego y por nivel.
- [ ] El filtro se refleja en la URL para poder compartirlo.

Depende de: [EM-012](#em-012)

#### EM-014

**Marcar contenido pendiente de revalidar al salir una nueva versión**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 5 · Ola: 5

> Como **tutor**, quiero saber qué lecciones quedaron probadas en una versión vieja cuando marco una nueva versión como actual, para mantener la promesa de que todo el contenido indica con qué versión funciona.

Criterios de aceptación:

- [ ] Al marcar una versión del juego como actual, las lecciones probadas en versiones anteriores pasan a `pendiente de revalidar`.
- [ ] Hay una vista para tutores con la lista de lecciones pendientes, agrupadas por curso.
- [ ] El alumno ve en la lección: `Probado en X. Pendiente de revalidar en Y`.
- [ ] Al revalidar, el tutor registra la nueva versión probada y la fecha.

Depende de: [EM-021](#em-021)

Nota: Es el diferenciador de la propuesta de valor ("ejemplos con versión comprobada"). Su costo real es de operación: alguien tiene que volver a probar.

### E2 Cursos y contenido

Estructura de cursos, módulos, lecciones y recursos descargables, para cualquier juego del catálogo.

#### EM-020

**Modelo de curso**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 3

> Como **administrador**, quiero crear cursos asociados a un juego, para ofrecer tanto la práctica corta (Misión Cero) como el curso de seis semanas.

Criterios de aceptación:

- [ ] Un curso tiene: título, slug, juego, tipo (`práctica corta` o `curso`), nivel, descripción, requisitos, duración en semanas y estado (`borrador` o `publicado`).
- [ ] El precio se captura en el curso (MXN, entero en centavos) y no está escrito en código.
- [ ] Solo los cursos publicados aparecen en páginas públicas.

Depende de: [EM-010](#em-010)

Nota: Precios del lienzo (MXN 199 Misión Cero, MXN 1,990 curso) son propuestas a probar, por eso se capturan como dato y no como constante.

#### EM-021

**Módulos y lecciones con versión probada**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 5 · Ola: 4

> Como **tutor**, quiero organizar un curso en módulos (uno por semana) y lecciones ordenadas, indicando con qué versión del juego y entorno se probó cada lección, para que el alumno siga una ruta clara y confiable.

Criterios de aceptación:

- [ ] Un curso tiene módulos ordenados; un módulo tiene lecciones ordenadas.
- [ ] La lección tiene título, contenido en Markdown, duración estimada en minutos y orden.
- [ ] La lección registra `probado con`: versión del juego, entorno de modding y fecha de prueba.
- [ ] El Markdown se convierte a HTML de forma segura (sin permitir scripts).

Depende de: [EM-020](#em-020), [EM-011](#em-011)

#### EM-022

**Vista previa de lecciones para tutores**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 3 · Ola: 8

> Como **tutor**, quiero ver cómo se verá una lección antes de publicarla, para corregir errores sin que los vean los alumnos.

Criterios de aceptación:

- [ ] Desde el admin hay un botón de vista previa que renderiza la lección igual que la verá el alumno.
- [ ] Las lecciones en borrador no son visibles para alumnos.

Depende de: [EM-021](#em-021), [EM-061](#em-061)

#### EM-023

**Recursos descargables y plantillas por lección**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 5

> Como **alumno**, quiero descargar la plantilla o el proyecto base de cada lección, para empezar a trabajar sin perder tiempo armando la estructura.

Criterios de aceptación:

- [ ] Una lección puede tener recursos: enlace (por ejemplo a un repo plantilla) o archivo.
- [ ] Cada recurso indica la versión del juego y del entorno para la que sirve.
- [ ] Solo los alumnos inscritos ven los recursos, salvo en lecciones de muestra.

Depende de: [EM-021](#em-021)

Nota: Para el piloto basta con enlaces. Subir archivos depende de EM-007.

#### EM-024

**Lección de muestra gratuita**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 5

> Como **visitante**, quiero ver una lección completa gratis antes de pagar, para comprobar si el estilo del curso me sirve.

Criterios de aceptación:

- [ ] Una lección puede marcarse como `muestra`.
- [ ] Las lecciones de muestra se ven sin cuenta y sin pago.
- [ ] La página del curso enlaza a su lección de muestra.

Depende de: [EM-021](#em-021)

### E3 Cuentas y datos personales

Registro, acceso, perfil y cumplimiento de privacidad.

#### EM-030

**Registro con correo y verificación**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 5 · Ola: 3

> Como **visitante**, quiero crear una cuenta con mi correo y contraseña, para poder inscribirme y guardar mi avance.

Criterios de aceptación:

- [ ] Formulario de registro con correo, nombre a mostrar y contraseña.
- [ ] Se envía un correo con enlace de verificación; sin verificar no se puede pagar.
- [ ] Correo duplicado muestra un error claro sin revelar datos de otra cuenta.
- [ ] Incluye la aceptación del aviso de privacidad (EM-033).

Depende de: [EM-003](#em-003), [EM-004](#em-004), [EM-033](#em-033)

#### EM-031

**Inicio de sesión, cierre y recuperación de contraseña**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 4

> Como **alumno**, quiero entrar, salir y recuperar mi contraseña, para acceder a mis cursos sin depender del equipo.

Criterios de aceptación:

- [ ] Inicio de sesión con correo y contraseña.
- [ ] Recuperación de contraseña por correo con enlace que expira.
- [ ] Mensajes y correos en español.

Depende de: [EM-030](#em-030)

#### EM-032

**Perfil del alumno**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 4

> Como **alumno**, quiero registrar mi usuario de Discord, mi usuario de GitHub y los juegos que me interesan, para que el tutor me encuentre en la comunidad y pueda revisar mis repositorios.

Criterios de aceptación:

- [ ] Página de perfil editable con nombre a mostrar, usuario de Discord, usuario de GitHub y juegos de interés.
- [ ] Los juegos de interés salen del catálogo (EM-010).

Depende de: [EM-030](#em-030), [EM-010](#em-010)

#### EM-033

**Aviso de privacidad y consentimiento**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 2

> Como **visitante**, quiero leer el aviso de privacidad y aceptarlo al registrarme, para saber qué datos se guardan y para qué.

Criterios de aceptación:

- [ ] Página pública `/privacidad/` con el texto vigente.
- [ ] Al registrarse se guarda la fecha y la versión del aviso aceptado.
- [ ] Si el aviso cambia de versión, se pide aceptarlo de nuevo al iniciar sesión.

Depende de: [EM-003](#em-003)

Nota: El texto legal es un entregable del equipo y debe revisarse contra la ley mexicana de protección de datos vigente. La plataforma solo lo muestra y registra la aceptación.

#### EM-034

**Solicitar baja de la cuenta y de los datos**

Tipo: Historia de usuario · Prioridad: Could · Release: R1 · Puntos: 3 · Ola: 5

> Como **alumno**, quiero pedir que se borre mi cuenta y mis datos, para ejercer mis derechos sobre mis datos personales.

Criterios de aceptación:

- [ ] Botón en el perfil para solicitar la baja, con confirmación.
- [ ] El administrador ve las solicitudes y puede ejecutarlas; los registros de pago se conservan anonimizados.

Depende de: [EM-032](#em-032)

### E4 Landing y venta

Páginas públicas, cobro con Stripe, cupos y devoluciones.

#### EM-040

**Landing de EngiMods**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 5

> Como **visitante**, quiero entender en una página qué es EngiMods, para qué juegos hay cursos y cómo empezar, para decidir si me inscribo al piloto.

Criterios de aceptación:

- [ ] Presenta la propuesta de valor: ruta en español, ejercicios pequeños, versión comprobada y revisión de lo que construyes.
- [ ] Muestra los juegos activos y los cursos publicados.
- [ ] Llamado a la acción hacia Misión Cero y hacia el grupo piloto.
- [ ] Funciona en teléfono.

Depende de: [EM-004](#em-004), [EM-012](#em-012)

#### EM-041

**Página de detalle del curso**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 6

> Como **visitante**, quiero ver el temario, precio, requisitos, duración y política de devolución de un curso antes de pagar, para saber exactamente qué compro.

Criterios de aceptación:

- [ ] Muestra temario (módulos y títulos de lecciones), precio en MXN, requisitos (computadora, juego, programación básica), duración y fechas del próximo grupo.
- [ ] La política de devolución es visible antes del botón de pago.
- [ ] Enlace a la lección de muestra.
- [ ] Si el grupo está lleno, el botón de pago se reemplaza por lista de espera (EM-046).

Depende de: [EM-020](#em-020), [EM-024](#em-024), [EM-050](#em-050)

Nota: El lienzo pide "precio, requisitos y devolución claros antes del pago".

#### EM-042

**Pago con Stripe Checkout**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 5 · Ola: 5

> Como **alumno con cuenta verificada**, quiero pagar un curso con tarjeta, para inscribirme a un grupo.

Criterios de aceptación:

- [ ] Al pagar se crea una sesión de Stripe Checkout con el precio del curso guardado en la base de datos.
- [ ] Se registra un `Pago` en estado `pendiente` ligado al alumno y al grupo.
- [ ] Páginas de éxito y de cancelación en español.
- [ ] No se puede pagar dos veces el mismo grupo.
- [ ] Probado en modo prueba de Stripe.

Depende de: [EM-009](#em-009), [EM-030](#em-030), [EM-050](#em-050)

#### EM-043

**Webhook de Stripe que confirma el pago e inscribe**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 5 · Ola: 6

> Como **sistema**, quiero confirmar el pago al recibir el aviso de Stripe, para que la inscripción dependa del pago real y no de que el alumno regrese a la página de éxito.

Criterios de aceptación:

- [ ] El endpoint verifica la firma del webhook.
- [ ] Al recibir `checkout.session.completed` el pago pasa a `pagado` y se crea la inscripción al grupo.
- [ ] Procesar el mismo evento dos veces no duplica nada (idempotente).
- [ ] Pruebas automatizadas con eventos simulados.

Depende de: [EM-042](#em-042), [EM-053](#em-053)

#### EM-044

**Correo de confirmación de compra**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 7

> Como **alumno**, quiero recibir un correo al confirmarse mi pago, para tener comprobante y saber los siguientes pasos.

Criterios de aceptación:

- [ ] Incluye curso, grupo, fechas, monto pagado y enlace a mi panel.
- [ ] Incluye cómo entrar a Discord (EM-080) y cómo preparar el laboratorio local (EM-063).

Depende de: [EM-043](#em-043), [EM-008](#em-008)

#### EM-045

**Cupo máximo por grupo**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 6

> Como **administrador**, quiero definir un cupo por grupo, para no vender más plazas de las que el tutor puede revisar.

Criterios de aceptación:

- [ ] El cupo se captura en el grupo (el lienzo propone 8).
- [ ] Con el grupo lleno no se crean nuevas sesiones de pago.
- [ ] Los pagos pendientes apartan lugar por un tiempo limitado configurable para evitar sobreventa.

Depende de: [EM-042](#em-042)

#### EM-046

**Lista de espera e interés por juego**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 3

> Como **visitante**, quiero dejar mi correo para el próximo grupo o para un juego que aún no tiene curso, para enterarme cuando abra.

Criterios de aceptación:

- [ ] Formulario con correo y juego o curso de interés.
- [ ] El administrador ve y exporta la lista, agrupada por juego.
- [ ] Requiere aceptar el aviso de privacidad.

Depende de: [EM-010](#em-010), [EM-033](#em-033)

Nota: Sirve como dato de demanda por juego: ayuda a decidir para qué juego hacer el siguiente curso.

#### EM-047

**Registrar devoluciones**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 3 · Ola: 7

> Como **administrador**, quiero registrar una devolución y quitar el acceso al curso, para cumplir la política de devolución sin hacerlo a mano en varios lugares.

Criterios de aceptación:

- [ ] Desde el admin se marca un pago como `devuelto` con motivo y fecha.
- [ ] La inscripción ligada se desactiva y se libera la plaza.
- [ ] El reembolso en Stripe se ejecuta desde la plataforma o se documenta el paso manual.

Depende de: [EM-043](#em-043)

#### EM-048

**Pago en efectivo en OXXO**

Tipo: Historia de usuario · Prioridad: Could · Release: R1 · Puntos: 3 · Ola: 7

> Como **alumno sin tarjeta**, quiero pagar en efectivo, para poder inscribirme aunque no tenga tarjeta.

Criterios de aceptación:

- [ ] Stripe Checkout ofrece OXXO como método de pago.
- [ ] La plaza se aparta mientras el pago está pendiente y se libera si vence.

Depende de: [EM-043](#em-043), [EM-045](#em-045)

Nota: Hipótesis no validada: que una parte del público no tiene tarjeta. Confirmar disponibilidad y comisión de OXXO en la página oficial de Stripe México antes de implementar.

#### EM-049

**Códigos de descuento**

Tipo: Historia de usuario · Prioridad: Could · Release: R1 · Puntos: 2 · Ola: 6

> Como **administrador**, quiero crear códigos de descuento, para ofrecer precio de piloto o promociones con aliados.

Criterios de aceptación:

- [ ] Se usan los códigos promocionales de Stripe Checkout.
- [ ] Se registra qué código usó cada pago.

Depende de: [EM-042](#em-042)

### E5 Grupos (cohortes)

Grupos de seis semanas con fechas, cupo, tutor y sesiones en vivo.

#### EM-050

**Crear grupos de un curso**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 4

> Como **administrador**, quiero abrir un grupo de un curso con fechas, cupo y tutor, para organizar cada generación de seis semanas.

Criterios de aceptación:

- [ ] Un grupo tiene curso, nombre, fecha de inicio, fecha de fin, cupo, tutor(es), enlace de Discord y estado (`inscripción abierta`, `en curso`, `cerrado`).
- [ ] Solo se puede pagar un grupo en `inscripción abierta`.

Depende de: [EM-020](#em-020), [EM-003](#em-003)

#### EM-051

**Liberar contenido por semana**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 3 · Ola: 8

> Como **tutor**, quiero que los módulos se liberen semana a semana según la fecha de inicio del grupo, para que el grupo avance al mismo ritmo y las clínicas tengan sentido.

Criterios de aceptación:

- [ ] El módulo N se libera en la fecha de inicio + (N-1) semanas.
- [ ] El tutor puede liberar un módulo antes de tiempo.
- [ ] Los módulos bloqueados muestran su fecha de liberación.

Depende de: [EM-050](#em-050), [EM-061](#em-061)

#### EM-052

**Calendario de clínicas grupales**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 7

> Como **alumno**, quiero ver las fechas y enlaces de las clínicas en vivo de mi grupo, para no perderme ninguna.

Criterios de aceptación:

- [ ] El tutor registra sesiones con fecha, hora (zona horaria de México), tema y enlace.
- [ ] El alumno las ve en su panel, ordenadas y con las pasadas marcadas.

Depende de: [EM-050](#em-050), [EM-060](#em-060)

#### EM-053

**Inscripciones e inscripción manual por administrador**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 5

> Como **administrador**, quiero inscribir a alguien a un grupo sin pasar por Stripe, para dar becas, hacer pruebas o registrar pagos cobrados por fuera durante el piloto.

Criterios de aceptación:

- [ ] Existe el modelo de inscripción (alumno, grupo, origen, estado activa/inactiva, fecha). Es el que usa después el webhook de Stripe (EM-043).
- [ ] Desde el admin se crea una inscripción con origen (`beca`, `prueba`, `pago externo`).
- [ ] Cuenta para el cupo del grupo.
- [ ] Queda distinguida de las inscripciones pagadas con Stripe en reportes.

Depende de: [EM-050](#em-050)

Nota: Permite correr el piloto aunque el flujo de pago (EM-042, EM-043) no esté listo.

### E6 Experiencia de aprendizaje

Lo que ve y hace el alumno inscrito: lecciones, progreso y laboratorio local.

#### EM-060

**Panel del alumno: mis cursos**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 6

> Como **alumno**, quiero ver mis cursos inscritos con mi avance, para retomar donde me quedé.

Criterios de aceptación:

- [ ] Lista de inscripciones activas con porcentaje de avance y siguiente lección.
- [ ] Enlace al Discord del grupo y a las clínicas.
- [ ] Si no tengo cursos, se muestra el catálogo.

Depende de: [EM-053](#em-053)

#### EM-061

**Ver una lección**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 7

> Como **alumno inscrito**, quiero leer una lección con su versión probada y sus recursos, para aprender y trabajar con confianza en que el ejemplo funciona.

Criterios de aceptación:

- [ ] Solo la ven alumnos inscritos en un grupo del curso (o cualquiera si es muestra).
- [ ] Muestra la etiqueta `Probado con <juego> <versión> + <entorno> <versión>`.
- [ ] Navegación a lección anterior y siguiente.

Depende de: [EM-021](#em-021), [EM-060](#em-060)

#### EM-062

**Marcar lección como completada**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 8

> Como **alumno**, quiero marcar una lección como completada, para llevar el control de mi avance.

Criterios de aceptación:

- [ ] Botón para marcar y desmarcar.
- [ ] El avance del curso se actualiza en el panel.

Depende de: [EM-061](#em-061)

#### EM-063

**Guía de laboratorio local por juego**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 3 · Ola: 7

> Como **alumno**, quiero una guía paso a paso para preparar mi computadora para hacer mods de mi juego, para no abandonar en la instalación.

Criterios de aceptación:

- [ ] Cada juego puede tener una guía de laboratorio con requisitos, pasos de instalación y una prueba final de que todo funciona.
- [ ] La guía indica para qué versión del juego y del entorno es válida.
- [ ] El alumno marca cada paso como hecho; el tutor ve quién está atorado.

Depende de: [EM-011](#em-011), [EM-060](#em-060)

Nota: El lienzo pone "ayudar con la instalación" como actividad clave y señala el abandono al encontrar errores como parte del problema.

### E7 Entregas y revisión

Envío de ejercicios y proyecto final, cola de revisión y rúbrica. Es el diferenciador principal frente a tutoriales sueltos.

#### EM-070

**Enviar una entrega**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 8

> Como **alumno**, quiero entregar un ejercicio con el enlace a mi repositorio, para recibir revisión de lo que construí.

Criterios de aceptación:

- [ ] Una lección puede definir un ejercicio entregable con instrucciones.
- [ ] La entrega incluye enlace al repositorio Git (obligatorio), comentario y la versión del juego y entorno que usé.
- [ ] Se valida que el enlace sea una URL de un servicio Git.
- [ ] El alumno ve el estado: `enviada`, `en revisión`, `aprobada`, `requiere cambios`.

Depende de: [EM-061](#em-061)

#### EM-071

**Cola de revisión con alerta de 24 horas**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 9

> Como **tutor**, quiero ver las entregas pendientes ordenadas por antigüedad, para cumplir la revisión en 24 horas que prometemos.

Criterios de aceptación:

- [ ] Lista de entregas pendientes de mis grupos, de la más vieja a la más nueva.
- [ ] Las que pasan de 24 horas se marcan en rojo.
- [ ] Se registra la hora de envío y la hora de revisión.

Depende de: [EM-070](#em-070)

Nota: Las 24 horas son una promesa del lienzo. Si el piloto muestra que no se cumple, hay que cambiar la promesa o el cupo.

#### EM-072

**Revisar con rúbrica**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 5 · Ola: 10

> Como **tutor**, quiero revisar una entrega con una rúbrica y comentarios, para dar retroalimentación consistente y de ingeniería, no solo "funciona o no funciona".

Criterios de aceptación:

- [ ] Cada ejercicio tiene una rúbrica con criterios (por ejemplo: funciona en la versión declarada, estructura, uso de Git, pruebas, documentación).
- [ ] El tutor califica cada criterio, deja comentario general y decide `aprobada` o `requiere cambios`.
- [ ] El alumno ve la revisión completa.

Depende de: [EM-071](#em-071)

#### EM-073

**Reenviar entrega tras cambios**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 11

> Como **alumno**, quiero reenviar mi entrega después de recibir cambios, para mejorar mi trabajo hasta aprobarlo.

Criterios de aceptación:

- [ ] Se conserva el historial de envíos y revisiones de la misma entrega.
- [ ] El reenvío vuelve a entrar a la cola con su propia hora de envío.

Depende de: [EM-072](#em-072)

#### EM-074

**Notificaciones de entregas por correo**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 11

> Como **alumno o tutor**, quiero recibir un correo cuando hay una entrega nueva o una revisión lista, para no tener que estar revisando la plataforma.

Criterios de aceptación:

- [ ] El tutor recibe correo al llegar una entrega a su grupo.
- [ ] El alumno recibe correo cuando su entrega es revisada.

Depende de: [EM-072](#em-072), [EM-008](#em-008)

#### EM-075

**Entregar archivo .zip**

Tipo: Historia de usuario · Prioridad: Could · Release: R1 · Puntos: 3 · Ola: 9

> Como **alumno que no usa Git todavía**, quiero subir mi proyecto como .zip, para poder entregar aunque aún no domine Git.

Criterios de aceptación:

- [ ] Alternativa al enlace, con límite de tamaño.
- [ ] El tutor puede descargarlo desde la revisión.

Depende de: [EM-070](#em-070), [EM-007](#em-007)

Nota: Contradice en parte la propuesta (Git es parte de lo que se enseña). Decidir si se ofrece.

#### EM-076

**Proyecto final con checklist de publicación**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 3 · Ola: 11

> Como **alumno**, quiero entregar mi mod final con un checklist de publicación, para dejarlo listo para publicarlo y mantenerlo.

Criterios de aceptación:

- [ ] El proyecto final pide: README, licencia, registro de cambios, versión compatible declarada y enlace a la publicación si ya existe.
- [ ] El tutor revisa el checklist como parte de la rúbrica.
- [ ] Se registra si el alumno publicó su mod y dónde.

Depende de: [EM-072](#em-072)

Nota: Es la evidencia directa de la hipótesis: "más personas terminarán y publicarán su primer mod funcional".

### E8 Comunidad y comunicación

Discord, avisos del curso y avisos de nuevas versiones del juego.

#### EM-080

**Acceso al Discord del grupo**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 1 · Ola: 7

> Como **alumno inscrito**, quiero ver el enlace de invitación al Discord de mi grupo, para unirme a la comunidad desde el primer día.

Criterios de aceptación:

- [ ] El enlace se muestra solo a inscritos del grupo, en el panel y en el correo de confirmación.

Depende de: [EM-050](#em-050), [EM-060](#em-060)

Nota: Integración automática con Discord (bot, roles) queda fuera del piloto.

#### EM-081

**Avisos del curso**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 3 · Ola: 5

> Como **tutor**, quiero publicar avisos para mi grupo, para comunicar cambios, recordatorios y nuevos retos.

Criterios de aceptación:

- [ ] El aviso aparece en el panel del alumno y se envía por correo.
- [ ] Se guarda el historial de avisos del grupo.

Depende de: [EM-050](#em-050), [EM-008](#em-008)

#### EM-082

**Aviso de nueva versión del juego a alumnos afectados**

Tipo: Historia de usuario · Prioridad: Could · Release: R1 · Puntos: 3 · Ola: 6

> Como **alumno**, quiero enterarme cuando sale una versión del juego que afecta lo que aprendí, para saber si mi mod necesita actualizarse.

Criterios de aceptación:

- [ ] Al revalidar lecciones (EM-014) se puede notificar a alumnos actuales y egresados del curso.
- [ ] El aviso dice qué cambió y qué lecciones se actualizaron.

Depende de: [EM-014](#em-014), [EM-081](#em-081)

### E9 Operación y métricas del piloto

Administración y medición de las hipótesis del piloto.

#### EM-090

**Admin configurado para operar el piloto**

Tipo: Técnica · Prioridad: Must · Release: R1 · Puntos: 2 · Ola: 9

Criterios de aceptación:

- [ ] Admin de Django en español con búsqueda y filtros para alumnos, pagos, inscripciones, grupos y entregas.
- [ ] Roles: `tutor` (ve sus grupos y entregas) y `administrador` (todo), usando grupos y permisos de Django.

Depende de: [EM-053](#em-053), [EM-070](#em-070)

#### EM-091

**Métricas del piloto**

Tipo: Historia de usuario · Prioridad: Must · Release: R1 · Puntos: 3 · Ola: 11

> Como **equipo EngiMods**, quiero ver las métricas que validan las hipótesis del piloto, para decidir con datos si el negocio sigue, cambia o se detiene.

Criterios de aceptación:

- [ ] Vista para administradores con, por curso y por grupo: registros, inscripciones pagadas, conversión de Misión Cero a curso, avance promedio, tasa de finalización, tiempo medio de revisión y, cuando EM-076 esté hecha, número de mods publicados.
- [ ] Cada número enlaza o explica cómo se calcula.
- [ ] Exportable a CSV.

Depende de: [EM-062](#em-062), [EM-072](#em-072)

Nota: El lienzo dice que el piloto debe comprobar interés, aprendizaje y disposición de pago. Sin esta vista no hay forma de comprobarlo.

#### EM-092

**Exportar datos operativos a CSV**

Tipo: Técnica · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 10

Criterios de aceptación:

- [ ] Exportar alumnos, inscripciones, avance y entregas de un grupo a CSV desde el admin.

Depende de: [EM-090](#em-090)

#### EM-093

**Encuesta de cierre del curso**

Tipo: Historia de usuario · Prioridad: Should · Release: R1 · Puntos: 2 · Ola: 7

> Como **equipo EngiMods**, quiero pedir a cada alumno una encuesta al terminar, para medir satisfacción, disposición a pagar el siguiente curso y si publicó su mod.

Criterios de aceptación:

- [ ] Se habilita al terminar el grupo y aparece en el panel del alumno.
- [ ] Las respuestas se ven en la vista de métricas (EM-091).

Depende de: [EM-060](#em-060)

### E10 Post-piloto

Lo que viene después de validar el piloto. No se trabaja en R1.

#### EM-100

**Membresía de actualizaciones**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **egresado**, quiero pagar una membresía para recibir contenido actualizado por versión, para mantener mis mods al día.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

Nota: Lienzo: "más adelante: membresía de actualizaciones". Requiere suscripciones de Stripe.

#### EM-101

**Talleres para grupos bajo cotización**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **administrador de un servidor o comunidad**, quiero solicitar un taller para mi grupo, para que mi equipo aprenda a hacer mods.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

Nota: Lienzo: "talleres para grupos bajo cotización". Inicia como formulario de solicitud.

#### EM-102

**Ruta introductoria para quienes empiezan de cero**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **persona sin conocimientos de programación**, quiero una ruta previa al curso principal, para poder entrar después al curso de seis semanas.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

Nota: Lienzo: "consideraremos una ruta introductoria posterior".

#### EM-103

**Portafolio público del alumno**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **egresado**, quiero una página pública con los mods que publiqué, para mostrar mi trabajo.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

#### EM-104

**Constancia de finalización verificable**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **egresado**, quiero una constancia con enlace de verificación, para demostrar que terminé el curso.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

#### EM-105

**Espacio para aliados y creadores**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **creador de mods aliado**, quiero revisar ejercicios y que se reconozca mi aporte, para colaborar con la academia.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

Nota: Lienzo, aliados clave: revisión de ejercicios a cambio de difusión y reconocimiento.

#### EM-106

**Varios tutores y reparto de revisiones**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **administrador**, quiero repartir automáticamente las entregas entre varios tutores, para escalar a más grupos sin romper las 24 horas.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

#### EM-107

**Facturación electrónica (CFDI)**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **alumno que necesita factura**, quiero solicitar mi factura desde la plataforma, para deducir o comprobar el gasto.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

Nota: Validar con un contador el régimen fiscal y si hace falta facturar desde el piloto. No está resuelto.

#### EM-108

**Plataforma en inglés**

Tipo: Historia de usuario · Prioridad: Later · Release: R2

> Como **persona de habla inglesa**, quiero usar la plataforma en inglés, para aprender aunque no hable español.

Criterios de aceptación:

- [ ] Por definir en refinamiento después del piloto.

Nota: El pitch habla de alcance internacional; el lienzo arranca con público hispanohablante en México.

## Hipótesis y decisiones abiertas

Nada de esta lista está validado. Cada punto afecta una o más historias y se resuelve antes de que esas historias entren a un sprint.

- **Qué juegos arrancan.** La plataforma es multi-juego desde el modelo (E1), pero cada juego exige lecciones propias probadas por versión y un tutor que lo domine. El lienzo calcula 36 horas de tutoría por grupo de seis semanas para un solo curso. Pendiente decidir con qué juegos abre el piloto. Afecta EM-006, EM-012, EM-040 y la carga de contenido.
- **Precios.** MXN 199 (Misión Cero, piloto), MXN 299 (Misión Cero después) y MXN 1,990 (curso) son propuestas del lienzo para probar. Por eso el precio es un dato del curso (EM-020) y no una constante en código.
- **Cupo y promesa de 24 horas.** Ocho plazas y revisión en 24 horas son promesas por validar en el piloto. EM-071 y EM-091 miden si se cumplen.
- **Comisión de Stripe.** El lienzo usa 3.6 % + MXN 3 por pago antes de IVA (consulta del 28/09/2026). Verificar de nuevo en la página oficial antes de abrir ventas.
- **Pago sin tarjeta (OXXO).** Supuesto: parte del público no tiene tarjeta. EM-048 queda como Could hasta tener evidencia.
- **Hosting y correo.** Sin elegir. EM-005 y EM-008 piden documentar costo con fuente y fecha; el gasto total del piloto está topado en MXN 1,500 según el lienzo.
- **Estilos del frontend.** Sin decidir (EM-004).
- **Aviso de privacidad, términos y política de devolución.** Los textos son entregables del equipo y deben revisarse contra la ley mexicana vigente. La plataforma solo los muestra y registra aceptación.
- **Facturación (CFDI).** No está claro si hace falta desde el piloto. Validar con un contador (EM-107).
- **¿Hace falta la plataforma para el piloto?** Un grupo de ocho personas se podría operar con un enlace de pago, Discord y un formulario. Construir la plataforma tiene valor propio (es parte de la clase y del producto), pero el piloto no debería esperar a que esté completa: EM-053 (inscripción manual) existe para eso.
