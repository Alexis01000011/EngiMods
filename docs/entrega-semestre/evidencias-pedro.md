# Evidencias de Pedro

## Aportación

Pedro implementó el modelo de usuario personalizado que sustenta el registro y la autenticación, configuró la conexión de Stripe en modo prueba que permitió construir el Checkout y el webhook encima, y coordinó el proyecto: backlog, asignaciones en GitHub Issues, revisiones de PR y decisiones de producto como el pivote multi-juego y la elección de los juegos del piloto.

| Historia | Aporte | Evidencia |
|---|---|---|
| EM-003 | App `accounts` con modelo de usuario personalizado por correo | Issue #3, PR #70, commit de5e7ad |
| EM-009 | Llaves de Stripe en modo prueba y documentación de Stripe CLI | Issue #9, PR #71, commit 3c7cda0 |
| Docs | Actualización de estado y pasos siguientes | PR #72 |

## EM-003: modelo de usuario personalizado

Creé la app `accounts` con un modelo `User(AbstractUser)` y un `UserManager` propio. El correo es el identificador principal (`USERNAME_FIELD = "email"`); se eliminaron `username`, `first_name` y `last_name` del modelo estándar de Django y se reemplazaron por `display_name`. La unicidad del correo no distingue mayúsculas, con una restricción en la base de datos (`UniqueConstraint(Lower("email"))`) y una búsqueda con `email__iexact` en el inicio de sesión.

El admin permite crear y editar usuarios con formularios basados en correo, con `list_display`, filtros y búsqueda. `createsuperuser` pide correo y nombre a mostrar, no username.

Esta es la primera migración del proyecto y la base sobre la que funcionan el registro (EM-030), la verificación de correo (EM-030), el inicio de sesión (EM-031), el consentimiento de privacidad (EM-033) y todo lo que identifica a un alumno o tutor. Sin un usuario por correo, el flujo de registro y verificación no tiene sentido.

**Cómo contarlo.** «Django trae un modelo de usuario con username, pero nuestro alumno se registra con correo. Creé un modelo personalizado donde el correo es el identificador y es único sin importar mayúsculas. Eso permite que el registro, la verificación y el inicio de sesión funcionen por correo electrónico, que es lo que el alumno ya tiene. Es la primera migración del proyecto: todo lo demás se construyó encima.»

**Evidencia.** [Issue #3](https://github.com/Alexis01000011/EngiMods/issues/3), [PR #70](https://github.com/Alexis01000011/EngiMods/pull/70) y [commit de5e7ad](https://github.com/Alexis01000011/EngiMods/commit/de5e7ad). Las pruebas están en [accounts/tests/test_user_model.py](https://github.com/Alexis01000011/EngiMods/blob/51e539c/accounts/tests/test_user_model.py). Para la demo, crear un usuario desde el admin con un correo en mayúsculas y mostrar que el inicio de sesión lo encuentra sin distinguir.

## EM-009: cuenta de Stripe en modo prueba

Configuré las tres llaves de Stripe (`STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`) como variables de entorno en `config/settings.py`, vacías por defecto para que el proyecto y la CI arranquen sin cuenta de Stripe. Actualicé `.env.example` con las tres variables documentadas.

Escribí `docs/stripe.md` con las reglas sobre las llaves, cómo obtener las de prueba, cómo instalar Stripe CLI en los tres sistemas operativos, cómo usar `stripe listen` y `stripe trigger`, las tarjetas de prueba y la diferencia con staging. Las pruebas verifican que las llaves se leen de las variables de entorno y que Django las oculta en sus reportes de error.

No agregué el SDK de Python de Stripe ni llamé a su API: eso lo hizo EM-042 (Checkout). Mi historia preparó la configuración y la documentación para que el equipo pudiera construir los pagos sin riesgo de exponer llaves.

**Cómo contarlo.** «Stripe necesita tres llaves que nunca deben estar en el código. Las configuré como variables de entorno con valores vacíos para que nada se rompa sin ellas. Escribí la guía de Stripe CLI para que cualquiera del equipo pudiera probar webhooks en local. El Checkout y el webhook se construyeron encima de esta configuración.»

**Evidencia.** [Issue #9](https://github.com/Alexis01000011/EngiMods/issues/9), [PR #71](https://github.com/Alexis01000011/EngiMods/pull/71) y [commit 3c7cda0](https://github.com/Alexis01000011/EngiMods/commit/3c7cda0). Las pruebas están en [core/tests/test_stripe_settings.py](https://github.com/Alexis01000011/EngiMods/blob/51e539c/core/tests/test_stripe_settings.py). La documentación en [docs/stripe.md](https://github.com/Alexis01000011/EngiMods/blob/51e539c/docs/stripe.md).

## Coordinación del proyecto

Además de las dos historias, coordiné el trabajo del equipo:

- **Backlog y asignaciones.** Mantuve `docs/BACKLOG.md` como fuente de verdad, con historias priorizadas por MoSCoW, dependencias y olas. Asigné historias en GitHub Issues para evitar colisiones entre los tres integrantes.
- **Decisiones de producto.** Participé en el pivote de Hytale a multi-juego, la elección de Minecraft: Java Edition y Hytale como juegos del piloto (17/11/2026), y las decisiones sobre Misión Cero autoguiada vs. por grupos.
- **Revisión.** Revisé PRs antes de merge para asegurar que cumplieran los criterios de aceptación y la Definition of Done.
- **Documentación de estado.** PR #72 actualizó el estado del proyecto después de las primeras integraciones.

La evidencia de coordinación está en el historial de issues y PRs del repositorio: asignaciones, comentarios de revisión y decisiones registradas.

## Qué puedo defender

- Por qué el usuario usa correo y no username, y cómo funciona la unicidad sin mayúsculas.
- Por qué las llaves de Stripe son variables de entorno y no constantes, y por qué se dejan vacías por defecto.
- Cómo se organizó el trabajo con el backlog, las olas y las asignaciones.
- Qué decisiones de producto se tomaron y cuáles siguen abiertas.
- Qué no está implementado: correo real, grupos, revalidación automática.
- Límites de la demo: datos de prueba, Stripe de prueba, correo por consola.

## Guion propuesto

**Apertura.** «Mi parte cubre las bases de autenticación y pagos, y la coordinación del proyecto.»

**Usuario.** «Implementé el modelo de usuario con correo como identificador. Django trae un usuario con username, pero nuestro alumno se registra con correo. La unicidad no distingue mayúsculas: si alguien se registra con Pedro@mail.com, no puede crearse otra cuenta con pedro@mail.com. Es la primera migración y la base de todo el flujo de cuentas.»

**Stripe.** «Configuré las tres llaves de Stripe como variables de entorno vacías. Escribí la guía para probar webhooks con Stripe CLI. El Checkout y la confirmación automática de pago se construyeron sobre esta configuración, sin que ninguna llave aparezca en el código.»

**Coordinación.** «Organicé el backlog con prioridades y dependencias, asigné las historias por área para evitar conflictos de migraciones, y participé en las decisiones de producto: el pivote a multi-juego, la elección de Minecraft y Hytale, y el modelo autoguiado para Misión Cero.»

**Límite.** «La demo usa Stripe de prueba y el correo sale por consola. No hay alumnos ni dinero real. El contenido tiene borradores de Minecraft sin probar en el juego. Lo que sí está completo es el ciclo técnico: de la landing a la revisión con rúbrica.»

## Fuentes

- [Repositorio (commit de referencia)](https://github.com/Alexis01000011/EngiMods/tree/51e539c)
- [Issue EM-003](https://github.com/Alexis01000011/EngiMods/issues/3) y [PR #70](https://github.com/Alexis01000011/EngiMods/pull/70)
- [Issue EM-009](https://github.com/Alexis01000011/EngiMods/issues/9) y [PR #71](https://github.com/Alexis01000011/EngiMods/pull/71)
- [PR #72](https://github.com/Alexis01000011/EngiMods/pull/72)
