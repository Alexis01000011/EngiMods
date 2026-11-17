# EngiMods: documentación técnica

## 1. Producto y alcance

EngiMods es una academia en línea en español para aprender a crear mods de videojuegos aplicando ingeniería de software: Git, pruebas, documentación, publicación y mantenimiento. No es un curso para copiar código; el alumno construye un mod y un tutor revisa lo que entrega.

El producto es multi-juego por diseño. Los juegos, sus versiones y los entornos de modding se guardan como datos del catálogo, no como casos especiales en el código. Cada lección puede declarar con qué combinación exacta fue probada. Ese es el diferenciador: contenido que dice con qué versión funciona; la revalidación automática aún no existe.

La oferta tiene dos piezas. **Misión Cero** es una práctica corta autoguiada, sin grupo ni fecha compartida, pensada como entrada de bajo precio. El **curso de seis semanas** es una oferta posterior, por grupos de hasta ocho alumnos, con clínicas y revisión de entregas. El alcance actual se centra en la primera; la segunda no está operativa.

El recorrido previsto de Misión Cero en staging usa Stripe en modo prueba: visitante, curso, registro, pago de prueba, inscripción, lección, entrega y revisión con rúbrica. No incluye alumnos ni dinero real. Puede mostrarse el flujo con datos de prueba identificados; para afirmar aprendizaje real de modding hace falta un ejercicio probado. El contenido completo de Misión Cero no se veía publicado en la observación pública del 16/11.

### MVP y MVE

En el material del curso, el MVP prueba el mecanismo de valor y el MVE prueba el recorrido de adopción. EngiMods tiene implementadas las piezas del mecanismo y del recorrido, pero no ha certificado la experiencia completa, ni con contenido real ni con datos de prueba.

| Etapa del MVE | Pieza implementada | Qué permite explicar | Límite observado 16/11 (sin reverificar) |
|---|---|---|---|
| Descubrir | Landing, listado de juegos, detalle de curso | Propuesta, catálogo, precio, requisitos y acceso | Solo se vio un juego y un curso ficticios |
| Iniciar | Registro, consentimiento, verificación, sesión, Checkout | Requisitos de cuenta y pago de prueba | Registro cerrado por aviso faltante; legal 404 |
| Recibir valor | Inscripción, lección, avance | Acceso por tiempo y etiqueta "Probado con" | El curso visible no mostraba temario publicado ni versión probada |
| Confiar y volver | Estado del pago, entrega, rúbrica, reenvío, panel y avance | Confirmación por webhook, retroalimentación y regreso al curso | No consta un ensayo del recorrido completo; no hay datos de retención |

La observación del 16/11/2026 fue de páginas públicas; no se revisó contenido privado ni borradores.

El recorrido se apoya en un monolito Django con siete apps.

## 2. Arquitectura

Es un monolito Django con plantillas renderizadas en el servidor. No hay API separada ni aplicación de frontend. El navegador recibe HTML y el CSS compilado; la lógica de acceso, pago y revisión vive en el servidor.

```text
Navegador
   | HTTPS
   v
Render: gunicorn + WhiteNoise
   |
   v
Django 5.2 y plantillas
   |-- apps: core, accounts, catalog, courses,
   |         enrollments, submissions, payments
   |-- PostgreSQL en Neon, por DATABASE_URL
   |-- Stripe Checkout y webhook, en modo prueba
   `-- correo por consola en desarrollo y staging
```

Render ejecuta la web con dos procesos de gunicorn y sirve los archivos estáticos con WhiteNoise. La base vive en Neon, separada del disco efímero de la web. Tailwind se compila durante el build y el CSS generado no se versiona. No hay Redis, workers, colas ni almacenamiento de archivos: las entregas son enlaces a repositorios Git.

La decisión evita administrar dos despliegues y mantiene una sola base de código para el piloto. También limita el alcance: no hay tareas en segundo plano, notificaciones automáticas ni procesamiento de pagos diferidos.

## 3. Aplicaciones y herramientas

### Aplicaciones

| App | Responsabilidad | Modelos principales | Estado |
|---|---|---|---|
| `core` | Inicio, salud, páginas legales, Markdown seguro y correo | LegalText | Implementada |
| `accounts` | Usuario, registro, verificación, sesión, rol de tutor y consentimiento | User, PrivacyConsent | Implementada |
| `catalog` | Juegos, versiones y entornos de modding | Game, GameVersion, ModdingEnvironment | Implementada |
| `courses` | Cursos, módulos, lecciones, "probado con", ejercicios y rúbrica | Course, Module, Lesson, LessonTest, Exercise, RubricCriterion | Implementada |
| `enrollments` | Inscripción, acceso por tiempo y avance | Enrollment, LessonProgress | Implementada |
| `payments` | Checkout y confirmación de pagos de Stripe | Payment | Implementada |
| `submissions` | Entregas, envíos, cola de revisión, rúbrica y reenvío | Submission, SubmissionAttempt, Review, ReviewScore | Implementada |
| cohorts, metrics | Grupos, calendario, avisos y reportes del piloto | Cohort, LiveSession, Announcement; sin modelos en metrics | Previstas, no existen |

Son siete apps implementadas. `cohorts` y `metrics` están en el diseño, no en el código. Por eso un curso de tipo "curso" todavía no se puede pagar: el Checkout lo bloquea hasta que existan los grupos.

### Stack

- Python 3.12+, Django 5.2 LTS y `uv` con `uv.lock`.
- PostgreSQL 17 en Neon para staging; SQLite en desarrollo. `django-environ` lee `DATABASE_URL` y las demás variables.
- Plantillas de Django y Tailwind CSS 4.3.4 mediante `django-tailwind-cli`, sin Node. Las fuentes se sirven localmente.
- Render gratuito para la web y Neon gratuito para la base, ambos en Ohio. gunicorn y WhiteNoise completan el despliegue.
- Stripe Checkout en modo prueba. La aplicación no recibe ni almacena datos de tarjeta.
- `pytest` con `pytest-django`, `ruff` para lint y formato, y GitHub Actions para las comprobaciones.
- Markdown con `markdown` y sanitización con `nh3`.

La CI revisa lint, formato, migraciones sin generar, pruebas, consistencia del backlog y enlaces de skills. Es una barrera útil, pero no sustituye una prueba manual del recorrido.

## 4. Recorrido principal

1. **Visita.** La landing muestra la propuesta, los cursos publicados y los juegos activos. El detalle del curso presenta temario, precio en MXN, requisitos, duración, días de acceso y política de devolución. Solo aparecen cursos y lecciones publicados.
2. **Registro.** `/registro/` exige que exista un aviso de privacidad vigente. Al registrarse se crea el usuario y su consentimiento, se inicia sesión y se envía un enlace de verificación por el backend de correo configurado. En staging ese backend es la consola.
3. **Verificación.** El enlace marca `email_verified_at`. Sin esa marca, `can_pay` es falso y el Checkout se bloquea. Para una demostración, el equipo puede leer el enlace en los logs o marcar la verificación desde el admin.
4. **Pago de prueba.** `/cursos/<slug>/pagar/` pide sesión. Antes de abrir Stripe revisa cuatro bloqueos: acceso vigente, curso por grupos, correo sin verificar y llaves de Stripe ausentes. Si no hay bloqueo, crea una sesión de Checkout con el precio guardado en centavos y registra un `Payment` pendiente con el id de sesión.
5. **Webhook.** `/pagos/stripe/webhook/` verifica la firma. Solo atiende `checkout.session.completed` con `payment_status = paid`. Marca el pago como pagado con el `amount_total` que reporta Stripe y crea la inscripción con origen `stripe` y fecha de fin de acceso. La página de éxito no inscribe.
6. **Inscripción y acceso.** `/mi-panel/` lista los cursos con acceso vigente y separa los vencidos. El acceso se calcula: inscripción activa y fecha de fin en el futuro. "Vencida" no se guarda como estado.
7. **Lección.** `/cursos/<slug>/lecciones/<pk>/` muestra una lección publicada con su etiqueta "Probado con" y navegación anterior/siguiente. El avance se marca o desmarca desde `/mi-panel/lecciones/<pk>/completada/`.
8. **Entrega.** `/mi-panel/entregas/lecciones/<lesson_pk>/` recibe un enlace a un repositorio Git, un comentario y la versión y entorno usados. El enlace se valida contra los servicios permitidos. La entrega queda ligada a la inscripción, no solo al usuario.
9. **Revisión y reenvío.** `/tutoria/entregas/` muestra la cola de pendientes, de la más antigua a la más nueva. Al abrir una entrega, queda "en revisión" y se registra el tutor. La revisión califica cada criterio de la rúbrica, deja un comentario y decide "aprobada" o "requiere cambios". Si pide cambios, el alumno puede reenviar; se conserva el historial y la entrega vuelve a la cola.

El correo de confirmación de compra y las notificaciones de entrega no forman parte de este recorrido. Siguen fuera del corte.

## 5. Permisos y controles

### Cuentas y roles

El usuario usa el correo como identificador, sin `username`, y lo normaliza sin distinguir mayúsculas. `is_tutor` es un rol de producto; `is_staff` es acceso al admin de Django. No son equivalentes.

Las pantallas de tutoría se protegen con una sola regla, `has_tutor_access`: cuenta autenticada, activa y con `is_tutor` o `is_superuser`. Se aplica con un decorador o un mixin. Quien no cumple recibe 403, incluido un usuario `is_staff` que no sea tutor. Un tutor tampoco obtiene acceso al admin por su rol. El superusuario es la excepción operativa. Esto evita que cada historia de tutoría invente su propia comprobación.

### Contenido y acceso

Los cursos y lecciones en borrador no se muestran y responden 404. Una lección solo se ve con una inscripción activa y vigente; los tutores y administradores también pueden verla. El panel muestra únicamente las inscripciones de la persona. El avance y las entregas se ligan a la inscripción propia. El reenvío solo se habilita si la entrega está en "requiere cambios" y la inscripción sigue vigente.

La cola de tutoría muestra todas las entregas pendientes mientras no existan grupos. Cuando lleguen las cohortes, el reparto por grupo tendrá que añadirse. Solo el tutor que tomó una revisión puede guardarla; otro tutor no puede enviar el formulario por ella. Esta regla se comprueba en la vista y se protege con transacción y bloqueo de fila.

### Pagos

La aplicación no maneja números de tarjeta: redirige a Stripe Checkout. El webhook valida la firma con `STRIPE_WEBHOOK_SECRET`; una firma inválida responde 400 y un secreto ausente responde 500. Solo un pago realmente pagado crea inscripción. El monto se toma de Stripe, no del precio actual del curso.

La idempotencia se apoya en el id único de la sesión de Checkout, en el estado del pago y en un bloqueo de fila durante la transacción. Procesar dos veces el mismo evento no duplica la inscripción. Si el alumno ya tenía acceso vigente, el pago se registra y se deja un aviso para revisar una devolución manual. No hay devoluciones automáticas ni pagos en efectivo.

### Datos, secretos y contenido

Los textos legales son versiones con fecha de vigencia. La versión vigente es la más reciente cuya fecha ya llegó. Si no hay texto vigente, `/privacidad/` y `/terminos/` responden 404 y el registro no abre. El código no inventa el contenido: lo captura el equipo en el admin.

El contenido Markdown se convierte y se sanitiza con `nh3`: sin scripts, atributos de evento ni enlaces `javascript:`. El dinero se guarda en centavos enteros de MXN. Pagos, inscripciones, entregas y revisiones usan `PROTECT` para no borrar historial. Los secretos viven en variables de entorno; el repositorio solo incluye `.env.example` con valores de ejemplo. En staging se activan redirección a HTTPS, cookies seguras y HSTS, y una prueba revisa `check --deploy`.

No se hizo una auditoría de seguridad ni una prueba de penetración. Los controles anteriores son los que se pueden leer en el código y en la configuración de esa base.

## 6. Requisitos y estado

El backlog marca 29 historias como hechas. La tabla las agrupa por área; cada ID conserva su trazabilidad en el backlog y en su issue.

| Área | Historias | Estado |
|---|---|---|
| Fundaciones | EM-001, EM-002, EM-003, EM-004, EM-005, EM-009 | Hecho |
| Catálogo | EM-010, EM-011 | Hecho |
| Contenido | EM-020, EM-021 | Hecho |
| Cuentas y legal | EM-030, EM-031, EM-033, EM-035, EM-036 | Hecho |
| Venta | EM-040, EM-041, EM-042, EM-043 | Hecho |
| Inscripción y aprendizaje | EM-053, EM-060, EM-061, EM-062, EM-064 | Hecho |
| Entregas y revisión | EM-070, EM-071, EM-072, EM-073, EM-077 | Hecho |

De esas 29, **25 forman el bloque A del recorte y suman 80 puntos**. Las otras cuatro son EM-001 y EM-002, de la ola 0, y EM-036 y EM-073, del bloque B. El bloque A está completo según el backlog. Los 80 puntos son una estimación de complejidad relativa: no son horas, no son un porcentaje de la calificación y no deben presentarse como avance medido.

"Hecho" significa que se cumplieron los criterios de la historia. No significa que el contenido esté cargado ni que la experiencia esté ensayada. Por ejemplo, EM-036 implementa la página de términos y su enlace, pero el texto legal vigente sigue pendiente de que el equipo lo aporte y lo apruebe.

## 7. Decisiones y exclusiones

| Decisión | Estado | Contenido | Efecto práctico |
|---|---|---|---|
| ADR 0001, stack base | Aceptada | Django 5.2 LTS, Python 3.12, uv, SQLite y PostgreSQL, pruebas y CI | Entorno Python gestionado por uv; la CI revisa cada cambio |
| ADR 0002, estilos | Aceptada | Tailwind 4 con django-tailwind-cli y la identidad de DESIGN.md | Sin Node; el CSS se compila y no se versiona |
| ADR 0003, hosting | Aceptada | Render gratuito para web y Neon gratuito para PostgreSQL | Staging sin costo, con suspensión por inactividad |
| ADR 0004, correo | Propuesta | Evaluar Resend o Brevo; falta decisión del equipo | No hay proveedor ni dominio elegidos; el correo sigue en consola |

El correo real salió del corte. EM-008 se cerró como no planeada (`NOT_PLANNED`) el 14 de noviembre y EM-044 quedó fuera porque depende de ella. La issue de EM-044 todavía aparece en la milestone `Semestre`, pero la decisión documentada en el backlog la deja fuera del alcance actual. El ADR 0004 sigue siendo una propuesta; no se creó cuenta, no se verificó dominio y no se enviaron correos externos.

Tampoco forman parte del producto actual:

- Grupos, cupos, calendario, Discord y curso de seis semanas. `cohorts` no existe y un curso por grupos no se puede pagar.
- Revalidación automática al salir una versión nueva. Solo se registra "probado con"; EM-014 y EM-082 están pendientes. No se debe prometer que el sistema marca o avisa por sí solo.
- Pagos en efectivo, pagos diferidos, devoluciones y códigos de descuento. Solo se atiende tarjeta o Link en modo prueba y el evento `checkout.session.completed`.
- Archivos `.zip` o almacenamiento de archivos. Las entregas son enlaces a repositorios Git.
- Lección de muestra gratuita, lista de espera, página completa de cada juego, métricas y encuesta de cierre. La ficha básica de juego existe desde EM-010, pero EM-012 sigue pendiente.
- React, Supabase o Cloudflare. Pertenecen a documentos anteriores al pivote técnico y no describen esta base.

## 8. Verificación

La revisión estática del 17 de noviembre de 2026 tomó como base el commit `539f1e0a866571d11ee7b53f9e14d946f4f33a74`.

| Comprobación | Fecha | Resultado | Alcance |
|---|---|---|---|
| CI del commit base | 14/11/2026 | Éxito; ejecución 43632455645 | Lint, formato, chequeo de migraciones, pruebas, backlog y skills |
| PR #115 | 14/11/2026 | Integrado | Cambio de documentación y recorte de EM-008 |
| Pruebas automatizadas | 14/11/2026 | 519 reportadas en el PR #115 | No se volvieron a ejecutar en esta revisión |
| Revisión estática | 17/11/2026 | Código y documentos leídos en el SHA de corte | Sin ejecutar la aplicación |
| Staging público | 16/11/2026 | Health y landing responden; legal 404; registro cerrado; curso ficticio sin temario publicado | GET de solo lectura; no se repitió |
| Restauración de base | 09/11/2026 | Reportada en docs/despliegue.md | No se repitió |

La CI y el historial de fusiones sostienen que el repositorio pasaba las comprobaciones automatizadas de esa ejecución. No certifican una demo actual ni la calidad del contenido. Tampoco se ejecutaron aquí `pytest`, migraciones, pagos ni pruebas de navegador. El número de 519 pruebas es un reporte del PR #115, no una medición propia de esta revisión.

En staging, la observación pública del 16 de noviembre encontró el servicio arriba, pero con un juego y un curso ficticios. El curso se anunciaba como "Curso ficticio para probar el pago", sin versión probada, y su detalle decía que el temario no estaba publicado. El registro mostraba que todavía no abría por falta de aviso de privacidad. Esa observación es histórica y no se reverificó para este documento.

## 9. Límites actuales

- El registro público está bloqueado mientras no exista un aviso de privacidad vigente. Cargar un texto inventado no es una solución aceptable.
- La observación pública del 16/11/2026 mostró un juego y un curso ficticios, sin versión probada ni temario publicado. Eso alcanza para explicar el flujo, no para afirmar aprendizaje real de modding.
- El correo sale por consola. La verificación y la recuperación de contraseña dependen de leer un enlace en los logs o de una acción del administrador.
- La web y la base gratuitas se suspenden por inactividad. La primera visita puede tardar; hay que abrir el sitio antes de la demo.
- No hay grupos ni métricas. No se puede afirmar retención, conversión, ingresos ni validación comercial con datos de la plataforma.
- El juego inicial, los días de acceso, el precio definitivo y los textos legales siguen abiertos. Los MXN 100 y 30 días del curso ficticio son datos de prueba, no la oferta comercial.
- El recorrido autenticado de compra, webhook, entrega y revisión no se reprodujo en la verificación del 16 de noviembre. La arquitectura y las pruebas lo soportan, pero la demo completa sigue pendiente.

## 10. Recorrido de demostración

1. Abrir staging varios minutos antes y confirmar `/health/`.
2. Usar cuentas de demostración; no crear personas ni pagos reales.
3. Si la demo abrirá registro, confirmar que el equipo aprobó y cargó aviso de privacidad y términos, y que ya no responden 404; si no, declarar que se usan cuentas preparadas.
4. Definir si la demo usará un juego y una práctica reales o datos de prueba identificados. Si se afirma aprendizaje real, cargar juego, versión, entorno, práctica, lección, ejercicio y rúbrica, y probar el ejercicio.
5. Si hay lección publicada, verificar "Probado con" y temario; si se usan ejemplos, etiquetarlos y no presentarlos como curso real.
6. Probar registro, consentimiento y verificación; si el registro sigue cerrado, decirlo y usar una cuenta preparada.
7. Hacer un pago con la tarjeta de prueba 4242 y confirmar que la inscripción la crea el webhook, no la página de éxito.
8. Mostrar panel, avance, entrega con enlace Git, cola del tutor, rúbrica y reenvío.
9. Mostrar un 403 con una cuenta que no sea tutora y explicar la diferencia entre tutor y staff.
10. Si algo falla, mostrar el estado real y el límite; no simular un pago ni un correo.

## 11. Aspectos por confirmar

El equipo debe confirmar la ruta de la demo, si usará contenido real o ejemplos identificados, los textos legales y su responsable, el juego y los días de acceso, y si se mostrará registro abierto o cuentas preparadas. También queda pendiente ensayar el recorrido y registrar el resultado.

## Fuentes

Consulta de fuentes públicas: 17 de noviembre de 2026. Los archivos del repositorio se citan en el SHA de corte.

- [Repositorio en el SHA de corte](https://github.com/Alexis01000011/EngiMods/tree/539f1e0a866571d11ee7b53f9e14d946f4f33a74)
- [README](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/README.md) y [pyproject.toml](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/pyproject.toml)
- [Arquitectura](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/docs/arquitectura.md) y [Product Backlog](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/docs/BACKLOG.md)
- [Despliegue](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/docs/despliegue.md) y [Stripe en modo prueba](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/docs/stripe.md)
- [Decisiones técnicas](https://github.com/Alexis01000011/EngiMods/tree/539f1e0a866571d11ee7b53f9e14d946f4f33a74/docs/decisiones) y [flujo de CI](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/.github/workflows/ci.yml)
- [PR #115](https://github.com/Alexis01000011/EngiMods/pull/115), [issue EM-008](https://github.com/Alexis01000011/EngiMods/issues/8) y [issue EM-044](https://github.com/Alexis01000011/EngiMods/issues/29)
- [Ejecución de CI del commit base](https://github.com/Alexis01000011/EngiMods/actions/runs/43632455645) y [staging, observación histórica del 16/11/2026](https://engimods-staging.onrender.com)
