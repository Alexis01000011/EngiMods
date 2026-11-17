# Evidencias de Fabián

## Aportación

Fabián construyó la base del catálogo multi-juego, el registro de versiones y entornos de modding, y el rol de tutor con una protección común para sus pantallas. Las tres historias están cerradas y sus PR integrados.

| Historia | Aporte | Evidencia |
|---|---|---|
| EM-010 | App catalog y modelo de juego con visibilidad pública | Issue #10, PR #75, commit 1532d91 |
| EM-011 | Versiones, entornos y compatibilidades por juego | Issue #11, PR #79, commit d06d405 |
| EM-035 | Rol de tutor y permiso compartido de tutoría | Issue #68, PR #76, commit dcc8b2b |

## EM-010: catálogo de juegos

Creé la app `catalog` y el modelo `Game`, con nombre, slug único, descripción corta, sitio oficial, logo por URL y estado activo u oculto. Agregué el admin con filtros, el listado público `/juegos/` y una ficha básica por slug, con pruebas de creación, validación, visibilidad, URLs y permisos. El juego se administra desde el admin; un visitante solo puede leer. Los activos aparecen en el listado y tienen ficha pública; los ocultos no se listan y su URL responde 404. El logo es una URL porque todavía no existe almacenamiento de archivos subidos; en un hosting con disco efímero, un archivo local se perdería al desplegar.

Es la primera pieza que hace que EngiMods sea multi-juego sin escribir lógica de un juego concreto. Un juego es un dato con visibilidad, no una rama de código. Ocultar permite retirar un juego del catálogo sin borrar sus cursos ni su historial.

**Cómo contarlo.** "El catálogo no decide qué juego existe en el código: lo registra el administrador. El estado activo u oculto controla qué se publica, y el slug sostiene una URL estable. Esa base es la que después permite asociar versiones, cursos y lecciones a un juego."

**Evidencia y pendiente.** [Issue #10](https://github.com/Alexis01000011/EngiMods/issues/10), [PR #75](https://github.com/Alexis01000011/EngiMods/pull/75) y [commit 1532d91](https://github.com/Alexis01000011/EngiMods/commit/1532d91018fc5197610b00ddb468722da0969cb2). Las pruebas están en [catalog/tests/test_games.py](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/catalog/tests/test_games.py). Para la demo, mostrar un juego activo en `/juegos/`, abrir su ficha y luego ocultarlo para comprobar el 404. En la observación pública del 16/11/2026 solo se veía un juego ficticio; no se revisó contenido privado. Usar un juego real o identificar claramente el dato de prueba.

## EM-011: versiones y entornos de modding

Agregué `GameVersion` y `ModdingEnvironment`. Una versión tiene número libre, fecha de publicación y marca de versión actual. Un entorno pertenece a un juego, tiene nombre y versión, y declara con qué versiones del juego es compatible. La validación impide mezclar versiones o entornos de juegos distintos, incluso al usar `add()` o `set()` sobre la relación. El admin permite crear, filtrar y muestra el error cuando una regla no se cumple.

El número de versión es texto libre; no se impone SemVer. Solo puede haber una versión actual por juego, con una restricción en la base y validación en el admin. La identidad del entorno es única por juego, nombre y versión. Todo se administra desde el admin; no hay escritura pública.

Sin este modelo, "probado con" sería una frase suelta. Con él, una lección puede apuntar a una versión del juego y a un entorno concretos, y la plataforma puede rechazar combinaciones incoherentes. Eso sostiene la promesa de contenido probado y prepara el terreno para una futura revalidación, aunque la revalidación automática todavía no existe.

**Cómo contarlo.** "No obligamos a que la versión sea SemVer porque cada juego publica como quiere. Lo que sí garantizamos es que solo haya una versión actual por juego y que un entorno solo declare compatibilidad con versiones de su mismo juego. La lección guarda la combinación exacta con la que se probó."

**Evidencia y pendiente.** [Issue #11](https://github.com/Alexis01000011/EngiMods/issues/11), [PR #79](https://github.com/Alexis01000011/EngiMods/pull/79) y [commit d06d405](https://github.com/Alexis01000011/EngiMods/commit/d06d40505a187bb27c0d5e59d85a62894a6214d6). Las pruebas están en [catalog/tests/test_versions.py](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/catalog/tests/test_versions.py). Para la demo, crear una versión y un entorno en el admin, asociar una compatibilidad y mostrar el rechazo de una versión de otro juego. En la observación pública del 16/11/2026 no se veían versiones reales ni una lección con "Probado con"; no se revisó contenido privado. El equipo debe decidir si prepara esos datos o si la demo usa ejemplos identificados.

## EM-035: rol de tutor

Agregué `is_tutor` al usuario, su migración y un módulo de permisos con `has_tutor_access`, un decorador y un mixin. El admin permite marcar o desmarcar tutores y filtrar la lista. Las pruebas cubren visitante, alumno, personal sin permiso, tutor, superusuario y cuentas inactivas.

La regla exige cuenta autenticada, activa y con `is_tutor` o `is_superuser`. Un usuario solo con `is_staff` recibe 403 en las pantallas de tutoría. Un tutor no obtiene acceso al admin por su rol. El superusuario sí pasa. La comprobación vive en un solo lugar para que las historias de tutoría no la repitan.

Tutor es un rol de producto, no un permiso de administración. Separarlo permite que un tutor revise entregas sin darle acceso a la configuración del sitio. También reduce el riesgo de que una pantalla nueva olvide la comprobación: usa el decorador o el mixin y hereda la misma regla.

**Cómo contarlo.** "Tutor no es lo mismo que staff. El staff entra al admin; el tutor entra a sus pantallas de revisión. Si una cuenta tiene staff pero no tutor, recibe 403. Centralizamos la regla para no tener una versión distinta en cada vista."

**Evidencia y pendiente.** [Issue #68](https://github.com/Alexis01000011/EngiMods/issues/68), [PR #76](https://github.com/Alexis01000011/EngiMods/pull/76) y [commit dcc8b2b](https://github.com/Alexis01000011/EngiMods/commit/dcc8b2baf2fcf375ab7f4131106452129228e4fb). Las pruebas están en [accounts/tests/test_tutor.py](https://github.com/Alexis01000011/EngiMods/blob/539f1e0a866571d11ee7b53f9e14d946f4f33a74/accounts/tests/test_tutor.py). Para la demo, entrar a `/tutoria/entregas/` con un tutor y con una cuenta staff que no sea tutora, para mostrar la diferencia entre 200 y 403. La cola necesita al menos una entrega; mientras no existan grupos, todos los tutores ven todas las pendientes.

## Otros PR de documentación

Además de las tres historias, Fabián tiene tres PR integrados que sostienen la base documental:

- [PR #77](https://github.com/Alexis01000011/EngiMods/pull/77): propone los ADR 0002, 0003 y 0004. Los dos primeros se aceptaron después; el 0004 sigue como propuesta. No se presenta como una decisión tomada en solitario.
- [PR #80](https://github.com/Alexis01000011/EngiMods/pull/80): sustituye el signo de sección por texto legible en la documentación.
- [PR #81](https://github.com/Alexis01000011/EngiMods/pull/81): actualiza el estado de los fundamentos y sus pendientes.

Estos PR no agregan funcionalidad. Sirven para explicar por qué el proyecto documenta sus decisiones antes de adoptarlas y para mantener el estado del repositorio legible.

## Qué puedo defender

- Cómo se representa un juego, una versión y un entorno como datos, sin lógica específica de un juego.
- Qué se publica y qué se oculta en el catálogo, y por qué ocultar no es borrar.
- Cómo se registra la combinación exacta con la que se probó una lección.
- Por qué tutor no equivale a staff y cómo se protege una pantalla con una regla común.
- Por qué las decisiones de estilos, hosting y correo se documentaron en ADR.
- Funciones que no están implementadas: revalidación automática y grupos.
- Correo real: fuera del corte; el envío sigue por consola.
- Pagos reales: no se usaron ni comprobaron; la demo prevista usa Stripe de prueba.
- Demo completa: no consta un ensayo de punta a punta con contenido o datos identificados.

## Guion propuesto

**Apertura.** "Mi parte se centra en el catálogo y el control de acceso de tutoría. El contenido de modding cambia con cada versión del juego, así que la plataforma guarda cada juego como dato, no como una excepción en el código."

**Catálogo.** "Implementé el modelo de juego, con estado activo u oculto y slug único. Después agregué versiones y entornos de modding. No obligamos a SemVer; solo una versión puede ser la actual por juego. Un entorno declara con qué versiones es compatible y la validación impide mezclar juegos distintos. Una lección puede indicar con qué combinación se probó."

**Tutor.** "También implementé el rol de tutor. No es lo mismo que personal del admin: una cuenta con `is_staff` pero sin `is_tutor` recibe 403 en las pantallas de tutoría. La regla está centralizada en un decorador y un mixin. El superusuario sí pasa."

**Evidencia y límite.** "La evidencia está en los PR 75, 79 y 76. La CI del commit base pasó, pero no demuestra por sí sola el recorrido completo. El 16 de noviembre, en la observación pública, se veían datos ficticios y no había temario publicado; no se revisó contenido privado y el registro estaba bloqueado por los textos legales. Falta ensayar la demo."

## Aspectos por confirmar

- Elegir o identificar el juego, la versión, el entorno y los días de acceso que se usarán en la demo.
- Publicar un aviso de privacidad y términos aprobados por el equipo si la demo abrirá registro; no inventar textos.
- Definir el alcance: si se afirma aprendizaje real, cargar una práctica con módulo, lección, ejercicio y rúbrica, y probar el ejercicio; si no, usar ejemplos identificados y declararlo.
- Preparar una cuenta de tutor y una cuenta staff sin rol de tutor para el contraste de permisos.
- Ensayar el pago de prueba y confirmar que la inscripción la crea el webhook.
- Abrir staging varios minutos antes por la suspensión del plan gratuito.
- No presentar las 519 pruebas del PR #115 como propias ni las cinco entrevistas como realizadas; la evidencia disponible es una conversación y cuatro casos simulados.

## Fuentes

La revisión estática del 17 de noviembre de 2026 tomó como base el commit `539f1e0a866571d11ee7b53f9e14d946f4f33a74`.

- [Repositorio en el SHA de corte](https://github.com/Alexis01000011/EngiMods/tree/539f1e0a866571d11ee7b53f9e14d946f4f33a74)
- [Issue EM-010](https://github.com/Alexis01000011/EngiMods/issues/10) y [PR #75](https://github.com/Alexis01000011/EngiMods/pull/75)
- [Issue EM-011](https://github.com/Alexis01000011/EngiMods/issues/11) y [PR #79](https://github.com/Alexis01000011/EngiMods/pull/79)
- [Issue EM-035](https://github.com/Alexis01000011/EngiMods/issues/68) y [PR #76](https://github.com/Alexis01000011/EngiMods/pull/76)
- [PR #77](https://github.com/Alexis01000011/EngiMods/pull/77), [PR #80](https://github.com/Alexis01000011/EngiMods/pull/80) y [PR #81](https://github.com/Alexis01000011/EngiMods/pull/81)
- [CI del commit base](https://github.com/Alexis01000011/EngiMods/actions/runs/43632455645) y [PR #115](https://github.com/Alexis01000011/EngiMods/pull/115)
- El documento `tecnico.md`, en esta misma carpeta, contiene el detalle de arquitectura y estado.
