# Arquitectura

Monolito Django con plantillas del lado del servidor. Sin API separada ni frontend aparte mientras el piloto no lo pida.

## Mapa de apps

Cada app es dueña de sus modelos y sus migraciones. Una historia normalmente toca una sola app; si toca otra, el PR lo dice explícitamente. Las apps se crean cuando llega la primera historia que las necesita (solo `core` existe hoy).

| App | Es dueña de | Modelos previstos | Historias |
|---|---|---|---|
| `core` | Plantilla base, landing, páginas estáticas y legales, textos legales versionados, utilidades compartidas (envío de correo) | `LegalText` (aviso de privacidad, términos y devolución) | EM-001, EM-004, EM-033 (texto), EM-036, EM-040 |
| `accounts` | Usuarios, rol de tutor, perfil, consentimiento de privacidad | `User`, `Profile`, `PrivacyConsent` | EM-003, EM-030 a EM-035 |
| `catalog` | Juegos, versiones, entornos de modding, guías de laboratorio | `Game`, `GameVersion`, `ModdingEnvironment`, `LabGuide`, `LabStep` | EM-010 a EM-014, EM-063 (contenido) |
| `courses` | Cursos y su contenido | `Course`, `Module`, `Lesson`, `LessonTest` (probado con), `LessonResource`, `Exercise`, `RubricCriterion` | EM-020 a EM-024, EM-041, EM-014 (estado de revalidación) |
| `cohorts` | Grupos y su calendario (solo cursos de tipo `curso`) | `Cohort`, `LiveSession`, `Announcement` | EM-050 a EM-052, EM-080, EM-081 |
| `enrollments` | Quién está inscrito, hasta cuándo tiene acceso y su avance | `Enrollment`, `LessonProgress`, `LabStepProgress`, `WaitlistEntry`, `ExitSurvey` | EM-053, EM-060 a EM-063, EM-046, EM-093 |
| `payments` | Cobros con Stripe y devoluciones | `Payment`, `Refund` | EM-009, EM-042 a EM-049 |
| `submissions` | Entregas y revisiones | `Submission`, `SubmissionAttempt`, `Review`, `ReviewScore` | EM-070 a EM-076 |
| `metrics` | Reportes del piloto (solo lectura, sin modelos propios) | Ninguno | EM-091, EM-092 |

Relaciones principales:

```
Game 1──* GameVersion
Game 1──* ModdingEnvironment *──* GameVersion (compatibilidad)
Game 1──* Course 1──* Module 1──* Lesson 1──* LessonTest ──> GameVersion + ModdingEnvironment
Lesson 1──* LessonResource
Lesson 1──0..1 Exercise 1──* RubricCriterion
Course 1──* Cohort                      (solo cursos de tipo "curso")
Course 1──* Enrollment *──1 User;  Enrollment *──0..1 Cohort
Enrollment 1──* LessonProgress
Exercise 1──* Submission *──1 Enrollment;  Submission 1──* SubmissionAttempt 1──0..1 Review 1──* ReviewScore
Payment ──> User + Course (+ Cohort si aplica); Payment confirmado crea Enrollment (origen = stripe)
LegalText 1──* PrivacyConsent ──> User, o correo si es lista de espera
```

## Reglas del modelo de datos

- **Multi-juego desde el modelo.** Nada se escribe pensando en un juego en particular. Si algo depende del juego (versiones, entorno, guía de laboratorio), se modela como dato del catálogo.
- **Dinero:** enteros en centavos de MXN (`price_cents`, `amount_cents`). Nunca `float`.
- **Precios, cupos y textos de negocio son datos**, no constantes en código. Están en hipótesis y van a cambiar.
- **Fechas:** `USE_TZ = True`, zona `America/Mexico_City`. Guardar siempre fechas con zona.
- **Usuario:** siempre `settings.AUTH_USER_MODEL` o `get_user_model()`, nunca `django.contrib.auth.models.User`.
- **Estados** con `models.TextChoices`, no cadenas sueltas.
- **Borrado:** `on_delete=PROTECT` para pagos e inscripciones; no se borra historial de dinero.
- **Inscripción sin grupo:** las prácticas cortas (Misión Cero) son autoguiadas. `Enrollment.cohort` y `Payment.cohort` son opcionales y solo se usan en cursos por grupos.
- **Acceso por tiempo:** la inscripción guarda su fecha de fin de acceso, calculada con los días de acceso del curso. El acceso vigente se calcula (inscripción `activa` y antes de esa fecha); "vencida" no se guarda como estado.

## Roles y pantallas

- **Administrador:** usa el admin de Django, incluido para capturar contenido (cursos, módulos, lecciones).
- **Tutor:** usuario marcado como tutor (EM-035). Revisa entregas, publica avisos, registra clínicas y revalida lecciones en pantallas propias, fuera del admin, protegidas con lo que ofrece `accounts`. Si además captura contenido, necesita acceso al admin con permisos sobre `courses`.
- **Alumno:** ve el contenido de un curso solo con acceso vigente (EM-053), salvo las lecciones de muestra.

## URLs públicas

En español y con slugs: `/juegos/<slug>/`, `/cursos/<slug>/`, `/cursos/<slug>/lecciones/<id>/`, `/mi-panel/`, `/privacidad/`, `/terminos/`. Cada app define `app_name` y las vistas se referencian con `reverse("app:nombre")`.

## Pagos

El acceso a un curso pagado depende del webhook de Stripe (EM-043), no de la página de éxito. El webhook es idempotente y verifica firma. La inscripción manual (EM-053) usa el mismo modelo `Enrollment` con otro origen.

- El id de la sesión de Checkout es único en `Payment` y es la llave de idempotencia.
- Solo se inscribe cuando la sesión llega con `payment_status = paid`. Los pagos diferidos (OXXO) se confirman con `checkout.session.async_payment_succeeded`.
- El monto pagado se toma de Stripe (`amount_total`), no del precio actual del curso.

## Correo

Funciones de envío centralizadas en `core` (por ejemplo `core/emails.py`) con plantillas en `templates/emails/`. En desarrollo se imprimen en consola.
