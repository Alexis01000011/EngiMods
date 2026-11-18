# Misión Cero: tu primer plugin para Hytale

**Estado: borrador para presentar; adaptador y paquete listos, prueba en juego pendiente.** El 18/11/2026 se compiló el adaptador contra el JAR oficial del servidor 0.7.7 con `javac 25.0.5.0.3`, se ejecutó el núcleo con `Pruebas del núcleo: OK` y se armó un JAR propio con `manifest.json` en la raíz. También se verificó que la clase `Main` extiende `JavaPlugin`, que tiene el constructor `JavaPluginInit` y que el manifiesto se decodifica con las clases oficiales. **No se arrancó el servidor, no se cargó el plugin en el juego y no se probó la conexión local.** La versión del cliente sigue sin confirmar. No crear `LessonTest` hasta completar esa prueba. La lección 1 es una muestra conceptual útil; su disponibilidad pública requiere que el equipo valide marca, estado y configuración. El curso práctico completo permanece bloqueado hasta resolver y probar L4 y L6 de punta a punta. Los tiempos son hipótesis.

D3, D6, D7, D8 y D9 del plan siguen abiertos: el plugin Java y este título son la **propuesta solicitada**, no una decisión de negocio ni de marca. Falta confirmar aviso y reglas antes de publicar o cobrar. EngiMods no está afiliado con Hypixel Studios; `[VERIFICAR: aviso y uso del nombre según políticas vigentes]`.

## Ficha de captura propuesta

| Modelo / campo | Valor propuesto |
|---|---|
| Game | Hytale; slug `hytale`; sitio https://hytale.com/; logo vacío; estado sujeto a decisión |
| GameVersion | Pendiente: registrar la versión exacta del cliente realmente ejecutada; fecha de publicación y marca de actual solo si se verifican. No crear un número ficticio. |
| ModdingEnvironment | Nombre propuesto: API de plugins de Hytale. Versión usada para compilar: JAR oficial del servidor 0.7.7. La compatibilidad en juego y la relación con GameVersion siguen pendientes de verificar. |
| Course | Título de arriba; slug `mision-cero-hytale`; práctica corta, principiante, `duration_weeks=1`, borrador. |
| Precio y acceso | **Pendientes**; `price_cents` y `access_days` son obligatorios. No capturar cero ni valores ficticios para sortear el bloqueo. |
| Descripción | Construye un comando de dados con Java, pruebas, Git y documentación; después conecta el núcleo a un plugin de servidor y entrega el repositorio para revisión. |
| Requisitos | Programación básica, computadora y permisos para instalar Java y Git; juego y cuenta legítima para la prueba real; conexión a internet y servidor local compatible. No se ha medido espacio ni memoria para cliente y servidor juntos. |
| Muestra | L1 `is_sample=True` cuando el equipo decida su publicación; no atribuirle un `LessonTest` que no exista. |
| Exercise | Solo L7; título `Tu primer plugin: el comando /dado`; instrucciones y cinco criterios en `ejercicio.md`; `is_final_project=False` para no activar el checklist de publicación de un mod público. El adaptador y el JAR de ejemplo existen; la prueba en juego del alumno sigue siendo obligatoria. |

| Módulo / orden | Lección / orden | Archivo | Minutos |
|---|---|---|---|
| 1. Antes de empezar / 1 | 1. Qué vas a construir | `leccion-1-que-vas-a-construir.md` | 10 |
| | 2. Prepara tu laboratorio | `leccion-2-prepara-tu-laboratorio.md` | 40 |
| 2. Tu primer plugin / 2 | 1. Crea tu proyecto | `leccion-3-crea-tu-proyecto.md` | 30 |
| | 2. Ejecuta el servidor local | `leccion-4-ejecuta-el-servidor.md` | 20 |
| | 3. El núcleo con pruebas | `leccion-5-el-nucleo-con-pruebas.md` | 45 |
| | 4. Conecta el núcleo | `leccion-6-conecta-el-nucleo.md` | 40 |
| 3. Entrega / 3 | 1. Documenta y entrega | `leccion-7-documenta-y-entrega.md` | 30 |

Total estimado: 215 minutos, sin tiempos de bloqueo ni descargas. Para `Lesson.content`, copiar **solo** lo posterior al marcador de cada lección. Quitar o resolver `[VERIFICAR]` antes de publicar la práctica. La guía de prueba y este archivo no son contenido de lección. El ejemplo fuente incluye el núcleo, sus pruebas, el adaptador y `manifest.json`; el código completo aparece en L5 y L6, de modo que la plataforma no necesita servir archivos del repositorio.

## Evidencia y límites (consulta: 18/11/2026)

- [Manual oficial del servidor](https://support.hytale.com/hc/en-us/articles/45326769420827-Hytale-Server-Manual), actualizado 12/10/2026: Java 25, archivos del launcher, autenticación, carpeta `mods/`, `--assets`, `--bind` y `--disable-sentry`. Advierte que por defecto escucha en `0.0.0.0:5520`. El formato de dirección de loopback y la conexión del cliente no se comprobaron; no se presenta un comando local como probado.
- [Documentación oficial](https://docs.hytale.com/) mostró `Release 0.7.7`; [metadatos Maven oficiales](https://maven.hytale.com/release/com/hypixel/hytale/Server/maven-metadata.xml) mostraron `release` 0.7.7. **No demuestra** que se haya probado la versión, ni que sea la versión instalada en el juego de una persona. No fijar `LessonTest` a partir de esto.
- [JavaPlugin](https://docs.hytale.com/api/com/hypixel/hytale/server/core/plugin/JavaPlugin.html) documenta su constructor con `JavaPluginInit`; [PluginBase](https://docs.hytale.com/api/com/hypixel/hytale/server/core/plugin/PluginBase.html) documenta `getCommandRegistry()`. La inspección del JAR 0.7.7 confirmó además `CommandBase.executeSync(CommandContext)`, `ArgTypes.STRING`, `withRequiredArg`, `context.get`, `context.sendMessage` y `Message.raw`. Son firmas de compilación; no acreditan carga, registro ni respuesta en el juego.
- El manifiesto externo se llama `manifest.json` y va en la raíz del JAR; el servidor 0.7.7 lo busca ahí para los `.jar` de `mods/`. Los campos y el esquema se contrastaron con `PluginManifest` y con los manifiestos incluidos en el JAR oficial. `ServerVersion: "0.7.7"` **no** es un rango válido en esta versión; se corrigió a `=0.7.7` y se decodificó con las clases oficiales. La coincidencia con `0.7.8` se rechaza.
- [Creación de contenido](https://docs.hytale.com/creating-content/) explica que los recursos pueden modificar contenido sin conocimientos de desarrollo. El plugin Java es otra ruta.
- El código `ejemplo/src/curso/dado/` es original de este borrador, no copia del ejemplo Minecraft. El 18/11/2026 se ejecutó el núcleo con `javac 25.0.5.0.3` y `java` de la misma instalación: salida `Pruebas del núcleo: OK`. El adaptador se compiló contra el JAR oficial 0.7.7, se armó `Dado-0.1.0.jar`, `jar --list` mostró `manifest.json` en la raíz y las clases esperadas, y un `URLClassLoader` cargó `curso.dado.hytale.DadoPlugin` como subclase de `JavaPlugin` con constructor `JavaPluginInit`. Es una verificación de compilación y empaquetado, no una prueba de servidor ni de juego.
- [Política de creadores](https://hytale.com/creator-policy) y [EULA](https://hytale.com/eula): revisar texto vigente, redistribución, marca y actividad comercial antes de publicar. No se afirma haber completado la revisión legal.

## Entrega al equipo

`guia-de-prueba.md` registra acciones, versiones, resultados y bloqueos. Antes de cargar la práctica: ejecutar L4 y L6 en un servidor aislado, confirmar la dirección de loopback, la autenticación oficial, la versión del cliente y la carga del plugin; completar la tabla de L6 en el juego; y repetir la lección con una segunda persona. Solo entonces se registra `LessonTest`. No cargar en base compartida desde este borrador. No copiar el JAR oficial del servidor, recursos, mundos ni configuraciones del juego al repositorio.
