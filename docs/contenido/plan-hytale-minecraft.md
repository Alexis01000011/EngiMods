# Plan de contenido: Hytale y Minecraft

Plan para producir el contenido de EngiMods para dos juegos: **Hytale** y **Minecraft: Java Edition**. Este documento **no es contenido**: define qué se va a escribir, cómo cabe en la plataforma, cómo se prueba y qué falta decidir. El contenido se escribe en otra sesión siguiendo este plan (sección 12).

- Decisión: el 17/11/2026 el equipo eligió Hytale y Minecraft: Java Edition como los juegos con los que arranca el piloto.
- Investigación: 17/11/2026. Las versiones y herramientas cambian rápido; la sección 7 dice qué se comprobó y qué falta verificar en fuentes oficiales.
- Lo que este plan propone y el equipo no ha decidido está en la sección 11, con una recomendación. Las decisiones que ya se tomaron están ahí mismo, con su fecha.
- Borradores de Minecraft: `docs/contenido/minecraft/` (17/11/2026), sin probar.

## 1. Qué se va a producir

| Producto | Por juego | Cuándo |
|---|---|---|
| **Misión Cero** (práctica corta, autoguiada) | Una por juego, con el mismo proyecto y la misma ruta | Ahora. Es lo que pide el recorte de semestre: Misión Cero de punta a punta en staging con al menos un juego. |
| **Curso de seis semanas** (por grupos) | Solo el temario | Después del semestre. Los grupos (EM-050) están fuera del recorte, así que hoy no se puede vender ni operar. |

Recomendación de orden: **Minecraft primero** para la demostración y Hytale después (decisión D1). Minecraft tiene herramientas estables y documentación oficial madura; Hytale está en acceso anticipado con actualizaciones frecuentes y su documentación oficial todavía está incompleta, así que su contenido se va a revalidar más seguido.

## 2. Cómo cabe en la plataforma

El contenido se captura como datos. Ningún texto, versión ni regla de un juego va en el código (`AGENTS.md`, secciones 1 y 6).

| Modelo (app) | Qué se captura | Notas para este plan |
|---|---|---|
| `Game` (`catalog`) | Nombre, slug, descripción corta, sitio oficial, estado | `logo_url` vacío: `DESIGN.md` pide no mostrar logo ni arte del juego. La descripción dice para qué sirve modear ese juego aquí, no publicidad del juego. |
| `GameVersion` | Número libre, fecha de publicación, si es la actual | Una sola actual por juego. Minecraft usa números como `26.3`. Para Hytale hay que decidir qué número se registra (sección 7). |
| `ModdingEnvironment` | Nombre, versión y versiones del juego compatibles | Un solo campo de versión (texto, 100 caracteres). Propuesta en la sección 7. |
| `Course` (`courses`) | Título, slug, juego, tipo, nivel, descripción, requisitos, semanas, precio en centavos, días de acceso, estado | Precio y días son hipótesis del piloto; los decide el equipo (D6). Título según las reglas de marca (sección 8). |
| `Module` | Título y orden | Ver temarios en las secciones 5 y 6. |
| `Lesson` | Título, contenido en Markdown, minutos estimados, orden, estado | La pantalla ya muestra título, "Probado con", minutos y "Entrega: [ejercicio]". El contenido no los repite. |
| `LessonTest` | Versión del juego, entorno y fecha con que se probó | **Solo se registra después de una prueba real** (sección 9). Sin ella la lección muestra "Sin versión probada". |
| `Exercise` | Título e instrucciones en Markdown | Uno por lección, como máximo. |
| `RubricCriterion` | Criterio, qué se revisa y orden | Lo ven el tutor al calificar y el alumno al leer su revisión. |
| `Submission` / `SubmissionAttempt` (`submissions`) | Enlace a un repositorio público (GitHub, GitLab, Bitbucket o Codeberg), versión del juego, entorno y comentario | Todo ejercicio termina en un repositorio Git. |

### Qué Markdown admite una lección

Se comprobó con `core.markdown.render_markdown` el 17/11/2026:

- **Sí:** títulos (`##` y `###`; el `#` lo ocupa el título de la lección), listas, tablas, bloques de código, citas, `<details>` con `<summary>`, `<kbd>` y enlaces.
- **Bloques de código, tablas y párrafos fuera de las listas.** Un bloque de código con sangría dentro de un paso numerado sale roto (se ve como código en línea y corta la lista). Escríbelos sin sangría entre dos pasos: la lista sigue con su número (`<ol start="3">`). Comprobado el 17/11/2026.
- **Dentro de `<details>` no se procesa Markdown.** Escribe su contenido en HTML: `<p>`, `<strong>`, `<code>` y `<pre><code>` con `<` y `>` escapados. Comprobado el 17/11/2026.
- **Sin listas de tareas:** `- [ ]` se ve como texto.
- **Bloques de código:** se quitan el nombre del lenguaje y las clases, así que no hay resaltado ni cabecera. Escribe la ruta del archivo en la línea anterior, por ejemplo: "En `src/main/java/.../Dado.java`:".
- **Sin clases CSS:** `callout-tip` y `margin-note` de `DESIGN.md` no se pueden usar dentro del contenido. Las notas van como cita (`> ※ ...`); las pistas y soluciones, en `<details>` ("Ver una pista", "Ver la solución").
- **Imágenes:** se aceptan por URL, pero no hay dónde alojarlas (EM-007 está fuera del semestre) y `DESIGN.md` no quiere arte del juego. El contenido se escribe para entenderse sin capturas.

### Lo que la plataforma aún no tiene y cómo se suple

| Falta | Historia | Mientras tanto |
|---|---|---|
| Recursos descargables por lección | EM-023 (bloque C) | El enlace al repositorio plantilla va en el texto de la lección, como ya dice el recorte. |
| Lección de muestra gratuita | EM-024 (bloque C) | Se escribe la lección 1 pensando en que sea la muestra. |
| Guía de laboratorio por juego | EM-063 (fuera del semestre) | La instalación es una lección (L2). |
| Ficha "Necesitas" de la lección | No modelada | Una sección `## Necesitas` dentro del contenido. |

## 3. Principios didácticos y plantillas

La identidad de EngiMods es enseñar a hacer mods **como se construye software**. Cada lección enseña algo del juego y algo de ingeniería a la vez.

**Principios:**

1. **Diseño hacia atrás.** Primero el resultado verificable de la lección; luego los pasos.
2. **Pasos pequeños y comprobables.** Cada paso tiene una acción y algo que el alumno puede ver ("Comprueba: en la consola aparece `...`").
3. **Primero el ejemplo y luego la práctica.** Un ejemplo resuelto, luego un cambio guiado y al final algo propio.
4. **El porqué antes del cómo.** Una frase de por qué se hace así antes de cada bloque de código.
5. **Git desde la primera lección.** Cada lección termina con un commit con mensaje sugerido.
6. **Errores reales.** La sección "Si algo falla" sale de lo que pasó al probar la lección (sección 9), no de errores imaginados.
7. **Versiones explícitas.** Cada comando y cada dependencia se escriben con la versión probada.
8. **Voz de EngiMods** (skill `disenar-pantalla`, "Voz y textos"): español de México, segunda persona, frases cortas, sin promesas ("domina", "garantizado"), y los errores dicen qué hacer. Los nombres de las API, las clases y los comandos se quedan en inglés dentro del código.

**Plantilla de lección** (secciones en este orden, en Markdown):

1. Párrafo de entrada, de dos o tres frases: qué vas a lograr y por qué importa.
2. `## Al terminar podrás`: de 2 a 4 logros observables.
3. `## Necesitas`: lo que debe estar listo antes (lecciones previas, programas y versiones).
4. Desarrollo: `##` por bloque y pasos numerados con "Comprueba:" al final de cada paso importante.
5. `## Si algo falla`: los errores encontrados en la prueba y qué hacer.
6. `## Cómo lo haría un equipo`: la práctica de ingeniería que se usó y por qué.
7. `## Guarda tu avance`: el commit sugerido y lo que sigue.

**Plantilla de ejercicio:** objetivo en una frase, punto de partida, pasos con "Comprueba:", qué entregar (URL del repositorio, *tag* y versión del juego y del entorno), cómo se revisa (los criterios de la rúbrica con palabras) y una lista para revisarse antes de enviar.

**Rúbrica base** (de 3 a 5 criterios, adaptada a cada ejercicio):

1. Funciona en la versión declarada.
2. La lógica tiene pruebas y pasan.
3. Uso de Git: commits pequeños con mensajes claros.
4. README que explica qué hace el mod, cómo instalarlo y con qué versión funciona.
5. Alcance: hace lo que pide el ejercicio, sin código copiado que no entienda.

## 4. Proyecto común: misma ruta, dos juegos

**Recomendación (D4): un comando de dados, `/dado 2d6`,** que tira dados y muestra el resultado en el chat.

- **Ingeniería real en pequeño.** La lógica (leer `2d6`, validar y tirar) es Java puro y se prueba con JUnit sin abrir el juego. El juego solo se conecta en una clase pequeña. Así se enseña a separar el núcleo del adaptador, que es la base de la arquitectura del curso.
- **Mismo núcleo en los dos juegos.** La clase del dado es casi idéntica en Minecraft y en Hytale; cambia el adaptador. Con eso el alumno ve en la práctica la idea multi-juego de EngiMods.
- **Sin arte ni recursos del juego.** No necesita texturas ni modelos, así que evita problemas de licencia y la regla de `DESIGN.md`.
- **Cabe en una tarde.** Encaja con una práctica corta.
- **Se puede revisar.** El tutor ve las pruebas, el README y el comando funcionando.

Alternativas, si el equipo prefiere algo más visual: un objeto o bloque nuevo (en Minecraft necesita una textura propia; en Hytale se puede hacer sin código con el editor de recursos), o un mensaje de bienvenida al entrar al servidor (más simple, con menos lógica que probar).

## 5. Misión Cero: temario propuesto

Misma estructura para los dos juegos; cambian los detalles de la última columna. Duración estimada total: de 3 a 4 horas, que se ajusta con las pruebas reales. `duration_weeks = 1`. Un solo ejercicio, al final, que es lo que revisa el tutor.

| Módulo | Lección | Al terminar podrás | Min (estimado) | Minecraft (Fabric) | Hytale (plugin Java) |
|---|---|---|---|---|---|
| 1. Antes de empezar | L1 Qué vas a construir y cómo se trabaja aquí | Explicar qué hace tu mod, qué es "Probado con" y cómo se entrega | 10 | Qué es un mod de Fabric y en qué se diferencia de un *datapack* | Qué es un plugin de servidor y en qué se diferencia de un pack sin código |
| | L2 Prepara tu laboratorio | Tener Java 25, IntelliJ IDEA Community, Git y una cuenta de GitHub listos y comprobados | 40 | Minecraft: Java Edition en la versión probada | Hytale y su servidor local; de dónde sale el `HytaleServer.jar` o la dependencia de Maven (verificar) |
| 2. Tu primer mod | L3 Crea tu proyecto desde la plantilla | Crear el proyecto, abrirlo en el IDE, entender sus archivos y hacer tu primer commit | 30 | `fabric.mod.json`, *entrypoint* y Gradle con Loom | `manifest.json`, clase principal del plugin y Gradle |
| | L4 Ejecuta el juego con tu mod | Arrancar el juego o el servidor con tu mod y comprobar en el registro que cargó | 20 | `runClient` | Servidor local con el plugin y conexión desde el juego |
| | L5 El núcleo: la lógica del dado con pruebas | Escribir la lógica en Java puro y comprobarla con JUnit antes de tocar el juego | 45 | Igual en los dos juegos | Igual en los dos juegos |
| | L6 Conecta el núcleo al juego | Registrar el comando `/dado` y ver el resultado en el chat | 40 | API de comandos de Fabric | Sistema de comandos de la API de plugins |
| 3. Entrega | L7 Documenta y entrega | Escribir el README, elegir licencia, declarar la versión, crear el *tag* `v0.1.0` y enviar tu entrega | 30 | Igual en los dos juegos | Igual en los dos juegos |

**Ejercicio (en L7):** "Tu primer mod: el comando `/dado`". Entrega: URL del repositorio, *tag* `v0.1.0`, versión del juego y del entorno. La rúbrica son los 5 criterios base de la sección 3.

**Lección de muestra (cuando exista EM-024):** L1, o L5 si se quiere mostrar la parte de ingeniería.

## 6. Curso de seis semanas: temario (solo plan)

El alumno extiende su mod de Misión Cero hasta tener un mod publicable y mantenible. Cada semana cierra con una entrega revisada por el tutor. Se detalla cuando se retomen los grupos (EM-050).

| Semana | Tema de ingeniería | Minecraft (Fabric) | Hytale |
|---|---|---|---|
| 1 | Arquitectura y flujo con Git: ramas, *pull requests* e *issues* | Organizar el mod en paquetes: núcleo y adaptadores | Lo mismo, con la estructura del plugin |
| 2 | Contenido por datos | Registros y generación de datos (en 26.3 cambian los registros recargables; verificar) | Recursos de datos en JSON, editor de recursos y modelos con Blockbench |
| 3 | Eventos, configuración y persistencia | Eventos de Fabric API y archivo de configuración | Eventos del servidor y configuración del plugin |
| 4 | Pruebas y calidad | JUnit y *game tests*; CI en GitHub Actions que compila y prueba | JUnit del núcleo, prueba manual guiada en servidor local y CI |
| 5 | Documentación, versiones y compatibilidad | Versionado semántico, CHANGELOG y versiones compatibles en `fabric.mod.json` | Versionado semántico, CHANGELOG y versión del servidor declarada |
| 6 | Publicación y mantenimiento | Modrinth y CurseForge; actualizar el mod a una versión nueva del juego | CurseForge (tienda oficial de mods de Hytale); actualizar a una versión nueva |

**Proyecto final:** con el checklist de EM-076 (README, licencia, registro de cambios, versión compatible declarada y enlace a la publicación).

## 7. Versiones y entornos a registrar

Captura del 17/11/2026, de fuentes oficiales cuando se pudo. **La sesión que escriba el contenido vuelve a confirmar cada número en la fuente oficial y anota la fecha.**

### Minecraft: Java Edition

| Dato | Valor | Fuente y estado |
|---|---|---|
| Versión estable | 26.3 (15/09/2026) | Blog oficial de Fabric. La 26.4 está en *snapshots*: al salir, toca revalidar. |
| Numeración | Por año y entrega: 26.1, 26.2, 26.3; correcciones como 26.3.1 | Fuentes secundarias coincidentes |
| Ofuscación | Desde 26.1 Minecraft ya no está ofuscado; Fabric usa los nombres oficiales de Mojang | Blog oficial de Fabric |
| Java | 25 como mínimo para desarrollar | Blog oficial de Fabric (26.1) |
| Fabric Loader | 0.19.5 | Blog oficial de Fabric (26.3) |
| Fabric API | 0.161.0+26.3; hay reportes de 0.162.0, sin confirmar | Modrinth; verificar |
| Loom y Gradle | Loom 1.17 y Gradle 9.6.0 | Blog oficial de Fabric (26.3) |
| Plantilla | Generador oficial de plantillas de Fabric | Verificar que ya genere proyectos para 26.3 |
| Alternativa | NeoForge con ModDevGradle (hay MDK para 26.1.2 y 26.2) | Documentación oficial de NeoForge; ver D2 |

**Cómo registrarlo:** `GameVersion` con número `26.3`. `ModdingEnvironment` con nombre `Fabric` y versión `Loader 0.19.5 · API 0.161.0+26.3`, compatible con `26.3`. El JDK y Gradle se dicen en la lección, no en el entorno.

### Hytale

| Dato | Valor | Fuente y estado |
|---|---|---|
| Estado | Acceso anticipado desde el 13/01/2026, con actualizaciones frecuentes | Sitio oficial y Wikipedia |
| Versión | La documentación oficial muestra "Release 0.7.2"; la Update 8 estaba en *pre-release* en octubre y noviembre de 2026 | **Sin confirmar** cuál es la versión estable hoy y cómo la numera el juego |
| Modos de modear | Plugins de servidor en Java y recursos de datos en JSON, con editor de recursos en el juego y Blockbench para modelos | Documentación oficial y comunitaria |
| Java | 25 | Guías comunitarias coincidentes; verificar en la oficial |
| API de plugins | Referencia de la API de Java en `docs.hytale.com`, todavía incompleta | Documentación oficial |
| Dependencia | `HytaleServer.jar` local o el repositorio Maven de Hytale; depende de la plantilla | **Sin confirmar** cuál es la forma oficial hoy |
| Plantillas | `HytaleModding/plugin-template` y otras de la comunidad | Comunitarias: revisar licencia y que estén al día |
| Código del servidor | Programa de código compartido solo para creadores seleccionados; no es público | Fuentes secundarias |
| Tienda de mods | CurseForge, oficial durante el acceso anticipado | Blog de CurseForge |

**Cómo registrarlo (propuesta):** `GameVersion` con el número que muestre el juego o el servidor en la versión estable, el mismo que use la documentación oficial. `ModdingEnvironment` con nombre `API de plugins de Hytale` y como versión la de la dependencia del servidor usada para compilar. Al ser acceso anticipado, cada lección de Hytale tiene que aislar las llamadas a la API en el adaptador (L6), para que una actualización toque una sola clase.

## 8. Marca, licencias y avisos

Cada punto se convierte en una revisión obligatoria del contenido (sección 9). **Hay que confirmar el texto vigente en las fuentes oficiales** antes de publicar.

- **Minecraft**
  - "Minecraft" no puede ser la primera palabra ni la parte dominante del título de un producto ni sugerir que es oficial. Ejemplo de forma válida: "Misión Cero: tu primer mod para Minecraft" (verificar).
  - El curso y su página llevan un aviso de que no es oficial ni está aprobado por Mojang ni asociado con Mojang. El texto exacto sale de las Usage Guidelines vigentes.
  - El EULA permite mods originales, pero no venderlos; los repositorios de los alumnos no incluyen código ni recursos de Mojang.
- **Hytale**
  - Seguir el EULA y las guías de uso de Hypixel Studios (no se encontró una guía de marca publicada; hay que buscarla en la fuente oficial).
  - Los recursos de Hytale no se reutilizan fuera del juego.
  - Aviso de que EngiMods no está afiliado con Hypixel Studios.
- **Los dos juegos**
  - Ningún repositorio (plantillas ni entregas) incluye los ejecutables ni los recursos del juego. El `.gitignore` de las plantillas los excluye.
  - Sin logos ni capturas con arte del juego en la plataforma (`DESIGN.md`).
  - Vender un curso que enseña a modear no es vender un mod, pero el equipo debe confirmar que las reglas de los dos juegos lo permiten antes de cobrar dinero real.

## 9. Cómo se produce cada lección

1. **Investigación.** Solo fuentes oficiales para versiones, API y reglas (lista al final), con fecha de consulta. Las comunitarias sirven para orientarse, pero lo que se enseña se comprueba.
2. **Borrador.** Con las plantillas de la sección 3, en el lugar que decida el equipo (D5).
3. **Prueba real.** Una persona del equipo con el juego sigue la lección tal cual en una máquina limpia (de preferencia Windows 11, que es lo más común en el público; anotar el sistema). Mide el tiempo real, anota cada error y la versión exacta del juego, el entorno, Java y Gradle. Los errores alimentan "Si algo falla".
4. **Revisión por pares.** Otra persona revisa con esta lista:
   - Sigue la plantilla.
   - Cada paso tiene su "Comprueba:".
   - Las versiones están escritas.
   - Cumple las reglas de marca.
   - Respeta la voz.
   - No contiene recursos ni código del juego.
5. **Carga.** En el admin: la lección en borrador, luego su `LessonTest` con la versión, el entorno y la fecha de la prueba, y al final se publica.
6. **Revalidación.** Cuando sale una versión nueva del juego o del entorno se repite la prueba y se agrega otro `LessonTest`. Mientras no exista EM-014, se lleva a mano.

**Una lección está lista cuando:** tiene la plantilla completa, se probó de punta a punta con las versiones registradas, otra persona la revisó, pasó la revisión de marca y tiene su `LessonTest`.

## 10. Repositorios plantilla

Uno por juego (D8). Cada uno con:

- Proyecto mínimo que compila con las versiones probadas.
- `.gitignore` que excluye binarios y recursos del juego.
- README de partida y licencia (propuesta: MIT, para que el alumno pueda publicar su mod).
- CI de GitHub Actions que compila y corre las pruebas.
- Una rama o *tag* por lección con el punto de llegada, para que quien se atore compare.

Los repositorios se marcan como plantilla de GitHub para que el alumno cree el suyo con un clic.

## 11. Decisiones del equipo

Decididas el 17/11/2026:

| # | Decisión | Qué se decidió |
|---|---|---|
| D1 | Qué juego va primero en la demostración | Minecraft: Java Edition. |
| D2 | Entorno de Minecraft | Fabric. NeoForge queda como opción del curso. |
| D4 | Proyecto de Misión Cero | El comando `/dado` (sección 4). |
| D5 | Dónde vive el contenido | En este repositorio, aunque es público: `docs/contenido/<juego>/`. Las lecciones se revisan en *pull requests* y se cargan en el admin a mano. |
| D6 | Precio y días de acceso de la Misión Cero de Minecraft | MXN 199 (`price_cents = 19900`) y 30 días de acceso. Sigue abierto si el precio incluye IVA. |
| D9 | Título del curso de Minecraft | "Misión Cero: tu primer mod para Minecraft". El texto del aviso se confirma en la fuente oficial (sección 8). |

Siguen abiertas:

| # | Decisión | Recomendación |
|---|---|---|
| D3 | Tipo de mod de Hytale | Plugin en Java: enseña la misma ingeniería que en Minecraft. Los recursos sin código entran en la semana 2 del curso. |
| D6 | Precio y días de acceso de la Misión Cero de Hytale | Abierto (hipótesis del piloto). |
| D7 | Quién prueba cada juego | Hace falta al menos una persona con cada juego comprado y una máquina donde probar. |
| D8 | Dónde viven los repositorios plantilla | Una cuenta u organización del equipo en GitHub, no una personal. Mientras no exista, la Misión Cero de Minecraft usa el generador oficial de plantillas de Fabric. |
| D9 | Título y aviso del curso de Hytale | Según la sección 8, confirmado en las fuentes oficiales. |

## 12. Instrucciones para la sesión que escriba el contenido

1. Lee este plan, `AGENTS.md`, `DESIGN.md` (sobre todo la voz) y la skill `disenar-pantalla`.
2. Confirma con la persona las decisiones de la sección 11 que sigan abiertas. No las supongas.
3. Verifica en las fuentes oficiales cada versión de la sección 7 y anota la fecha. Si la red de la sesión bloquea un dominio oficial, dilo; no lo sustituyas con fuentes comunitarias sin marcarlo.
4. Escribe primero el juego elegido en D1: las 7 lecciones de la sección 5, el ejercicio y su rúbrica, con las plantillas de la sección 3.
5. Escribe también, por lección, la guía de prueba para quien la va a probar: qué debe ver en cada paso y qué anotar.
6. No marques ninguna lección como probada ni crees su `LessonTest`: eso solo pasa después de la prueba real (sección 9).
7. No incluyas código, recursos ni capturas del juego, ni textos legales o de precios inventados.
8. Deja anotado en el borrador cada dato sin confirmar con `[VERIFICAR: ...]`.

## Fuentes consultadas (17/11/2026)

Oficiales:

- [Fabric para Minecraft 26.1](https://fabricmc.net/2026/03/14/261.html) y [Fabric para Minecraft 26.3](https://fabricmc.net/2026/09/15/263.html)
- [Documentación de Loom](https://docs.fabricmc.net/develop/loom/)
- [NeoForge para Minecraft 26.1](https://neoforged.net/news/26.1release/) y [primeros pasos de NeoForge](https://docs.neoforged.net/docs/gettingstarted/)
- [EULA de Minecraft](https://minecraft.net/eula) y [cambios al EULA y a las guías de uso comercial](https://www.minecraft.net/en-us/article/minecraft-eula-and-commercial-usage-guidelines-updates)
- [Documentación de Hytale](https://docs.hytale.com/)
- [Hytale ya está aquí (anuncio del acceso anticipado)](https://hytale.com/news/2026/1/hytale-is-finally-here) y [actualizaciones del juego](https://hytale.com/news/game-updates)
- [Preguntas frecuentes de Hytale en el blog de CurseForge](https://blog.curseforge.com/hytale-faq-answered-by-simon-and-slikey-from-hypixel-studios/)

Comunitarias o secundarias (orientación; verificar antes de enseñar):

- [Plantilla de plugin de HytaleModding](https://github.com/HytaleModding/plugin-template) y [documentación de HytaleModding](https://hytalemodding.dev/en/docs/established-information/server/content-categories/data-assets)
- [Configuración del entorno en Doctale](https://doctale.dev/getting-started/setup/)
- [Programa de código compartido de Hytale (The Escapist)](https://www.escapistmagazine.com/news-hytale-releases-server-source-code-assets-shared-source-programme/)
- [Versiones de Minecraft 26.x](https://minecrafthub.io/articles/latest-minecraft-version)
- [Resumen de las Usage Guidelines de Minecraft (ConductAtlas)](https://conductatlas.com/platform/minecraft/minecraft-usage-guidelines/)
