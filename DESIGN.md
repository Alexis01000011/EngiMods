---
version: alpha
name: EngiMods
description: Academia en línea para crear mods de videojuegos con ingeniería de software. Se ve como un buen libro de texto, cálido y bien hecho, con la estructura de una documentación técnica.
colors:
  primary: "#B83A0B"
  primary-hover: "#8F2D08"
  on-primary: "#FFFFFF"
  primary-container: "#FDF0E6"
  on-primary-container: "#5C2A10"
  primary-soft: "#F1D9CC"
  on-primary-soft: "#8F2D08"
  ink: "#2A2621"
  ink-soft: "#4A443C"
  ink-muted: "#6B645B"
  background: "#FBF8F3"
  surface: "#FFFFFF"
  surface-sunken: "#F5F0E8"
  surface-chip: "#F3EEE5"
  progress-track: "#ECE4D8"
  divider: "#E6DFD4"
  outline: "#8C8276"
  code-background: "#2A2621"
  code-text: "#F3EEE5"
  code-muted: "#CFC5B8"
  code-divider: "#423B34"
  tested: "#17663F"
  tested-container: "#E3F3EA"
  revalidate: "#7A4F00"
  revalidate-container: "#FFF1CC"
  error: "#B00F3A"
  error-container: "#FDE7EC"
typography:
  title-lg:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 2.75rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.015em
  title-md:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 2.125rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.015em
  headline-md:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 1.75rem
    fontWeight: 700
    lineHeight: 1.3
  headline-sm:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 1.375rem
    fontWeight: 600
    lineHeight: 1.35
  dek:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 1.3125rem
    fontWeight: 400
    lineHeight: 1.5
  reading-lg:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 1.25rem
    fontWeight: 400
    lineHeight: 1.75
  reading-md:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 1.1875rem
    fontWeight: 400
    lineHeight: 1.7
  wordmark:
    fontFamily: "'Source Serif 4', Georgia, serif"
    fontSize: 1.4375rem
    fontWeight: 700
    lineHeight: 1.2
  body-md:
    fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif"
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif"
    fontSize: 0.9375rem
    fontWeight: 600
    lineHeight: 1.25
  label-sm:
    fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif"
    fontSize: 0.8125rem
    fontWeight: 500
    lineHeight: 1.35
  eyebrow:
    fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif"
    fontSize: 0.75rem
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: 0.06em
  code-md:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: 0.9375rem
    fontWeight: 400
    lineHeight: 1.7
  code-sm:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: 0.8125rem
    fontWeight: 500
    lineHeight: 1.3
rounded:
  sm: 8px
  md: 12px
  lg: 16px
  full: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  gutter: 16px
  touch-target: 44px
  reading-max: 42.5rem
  sidebar: 18rem
  aside: 16rem
  nav-height: 64px
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
  nav-bar:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
    typography: "{typography.label-md}"
    height: "{spacing.nav-height}"
    padding: "{spacing.lg}"
  wordmark:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
    typography: "{typography.wordmark}"
  link:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
  text-soft:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink-soft}"
    typography: "{typography.dek}"
  text-muted:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.body-sm}"
  eyebrow:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.eyebrow}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: 22px
    height: 48px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: 20px
    height: "{spacing.touch-target}"
  button-quiet:
    backgroundColor: "{colors.surface-chip}"
    textColor: "{colors.ink}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: 14px
    height: "{spacing.touch-target}"
  chip:
    backgroundColor: "{colors.surface-chip}"
    textColor: "{colors.ink-soft}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 12px
    height: 32px
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 14px
    height: 48px
  input-field-border:
    backgroundColor: "{colors.outline}"
    height: 1px
  input-field-error:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.error}"
    typography: "{typography.body-sm}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  sidebar:
    backgroundColor: "{colors.surface-sunken}"
    textColor: "{colors.ink}"
    width: "{spacing.sidebar}"
    padding: "{spacing.md}"
  syllabus-item-current:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
  lesson-tile:
    backgroundColor: "{colors.progress-track}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.code-sm}"
    rounded: 10px
    size: 40px
  lesson-tile-current:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.on-primary-soft}"
    typography: "{typography.code-sm}"
    rounded: 10px
    size: 40px
  progress-bar:
    backgroundColor: "{colors.progress-track}"
    textColor: "{colors.primary}"
    rounded: 3px
    height: 6px
  avatar:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.on-primary-soft}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    size: 40px
  tested-stamp:
    backgroundColor: "{colors.background}"
    textColor: "{colors.tested}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.full}"
    size: 112px
  badge-tested:
    backgroundColor: "{colors.tested-container}"
    textColor: "{colors.tested}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.full}"
    padding: 12px
  badge-revalidate:
    backgroundColor: "{colors.revalidate-container}"
    textColor: "{colors.revalidate}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.full}"
    padding: 12px
  badge-untested:
    backgroundColor: "{colors.surface-chip}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.full}"
    padding: 12px
  outcomes-box:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.reading-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  callout-tip:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.on-primary-container}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 18px
  margin-note:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.body-sm}"
  code-block:
    backgroundColor: "{colors.code-background}"
    textColor: "{colors.code-text}"
    typography: "{typography.code-md}"
    rounded: "{rounded.lg}"
    padding: 18px
  code-block-header:
    backgroundColor: "{colors.code-background}"
    textColor: "{colors.code-muted}"
    typography: "{typography.label-sm}"
  code-inline:
    backgroundColor: "{colors.surface-chip}"
    textColor: "{colors.ink}"
    typography: "{typography.code-sm}"
    rounded: 4px
    padding: 4px
  divider:
    backgroundColor: "{colors.divider}"
    height: 1px
  message-success:
    backgroundColor: "{colors.tested-container}"
    textColor: "{colors.tested}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
  message-info:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.on-primary-container}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
  message-warning:
    backgroundColor: "{colors.revalidate-container}"
    textColor: "{colors.revalidate}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
  message-error:
    backgroundColor: "{colors.error-container}"
    textColor: "{colors.error}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
---

# DESIGN.md de EngiMods

Estado: **propuesta**, ligada al [ADR 0002](docs/decisiones/0002-estilos-frontend.md). Mientras el equipo no la acepte, no es obligatoria para EM-004 ni para ninguna pantalla.

Este archivo sigue el formato [DESIGN.md](https://github.com/google-labs-code/design.md) de Google Labs (versión `alpha`): los valores exactos están arriba, en YAML, y el texto explica cuándo y por qué se usan. Los títulos de sección van en inglés porque así los reconoce el formato; el contenido va en español. Si un valor y el texto no coinciden, manda el valor y se corrige el texto.

Para diseñar o maquetar una pantalla con este sistema, usa la skill `disenar-pantalla` (`.claude/skills/disenar-pantalla/`). Trae la anatomía de cada tipo de pantalla, las recetas de componentes y una página de referencia (`referencia/leccion.html`) que se abre en el navegador.

## Overview

EngiMods se ve como **un buen libro de texto, cálido y bien hecho, con la estructura de una documentación técnica**. Es un lugar donde da gusto aprender: nadie te obliga a estudiar un tema, te invitamos a construir algo tuyo.

La identidad se apoya en tres ideas:

- **Gusto por aprender.** La lectura es cómoda y cálida: papel crema, letra con serifa a buen tamaño y espacio para respirar. Cada lección empieza por lo que vas a poder hacer, no por la lista de temas. El avance se celebra sin hacer ruido.
- **Confianza.** Sabemos lo que enseñamos y lo decimos todo: con qué versión se probó, quién escribió y revisó la lección, cuándo, cuánto tarda, qué necesitas y qué vas a entregar. Nada queda en letra chica.
- **Humildad.** Te acompañamos, no te presumimos nada. El tutor aparece con su nombre, los errores se tratan como parte de aprender ("Si algo no sale a la primera, es parte de aprender") y no hay frases de venta ni promesas grandes.

Inspiraciones y lo que se tomó de cada una: de la interfaz japonesa, que todo esté explícito, con notas al margen (※) y un sello de "Probado", pero sin su saturación; de Medium, la columna de lectura y la línea de autor; de la documentación técnica moderna, el temario lateral, el índice "En esta lección" y los consejos; de YouTube, el avance visible por lección y el "continúa donde te quedaste".

Quien la lee es hispanohablante, casi siempre en México, sabe programar lo básico y muchas veces entra desde el teléfono. EngiMods enseña a hacer mods de varios juegos: la interfaz es la misma para todos y ningún juego le pone su color, su tipografía ni su arte.

## Colors

Papel cálido, tinta café oscuro y un solo acento terracota.

- **Background** {colors.background}: el papel crema de la página. Es el fondo de la lectura; la lección no va dentro de una tarjeta, va sobre el papel.
- **Surface** {colors.surface}: blanco para piezas que se separan del papel: tarjetas, el cuadro "Al terminar podrás", campos de formulario y la lección actual en el temario.
- **Surface sunken** {colors.surface-sunken}: el temario lateral, un papel un poco más oscuro. **Surface chip** {colors.surface-chip}: fondo de chips, código en línea y botones discretos.
- **Ink** {colors.ink}: texto principal y títulos. **Ink soft** {colors.ink-soft}: el subtítulo en cursiva y las frases de acompañamiento. **Ink muted** {colors.ink-muted}: metadatos, fechas, etiquetas y texto de ayuda; nunca para el texto de una lección.
- **Primary** {colors.primary}: terracota, el único acento. Es el color de lo que se puede tocar: enlaces, botones principales, el anillo de foco y el relleno de las barras de avance. Si algo es terracota, se puede usar o indica tu avance. **Primary hover** {colors.primary-hover} al pasar el puntero o presionar.
- **Primary container** {colors.primary-container} con {colors.on-primary-container}: consejos y avisos informativos. **Primary soft** {colors.primary-soft} con {colors.on-primary-soft}: el avatar del tutor y el cuadrito de la lección actual.
- **Divider** {colors.divider}: separadores y bordes de tarjetas. **Outline** {colors.outline}: borde de campos de formulario y botones secundarios, con contraste suficiente (3:1) para verse.
- **Progress track** {colors.progress-track}: el riel de las barras de avance y los cuadritos de lecciones pendientes.
- **Code** {colors.code-background}: los bloques de código son oscuros, como una terminal, con texto {colors.code-text}. Es el único bloque oscuro de la página y marca "esto se escribe en la terminal".

Cuatro colores de estado, siempre en pareja de texto y fondo claro y siempre con palabras:

- **Tested** {colors.tested} sobre {colors.tested-container}: "Probado con", lecciones completadas y mensajes de éxito. El sello de "Probado" también es verde, para no confundirse con el terracota interactivo.
- **Revalidate** {colors.revalidate} sobre {colors.revalidate-container}: contenido pendiente de revalidar porque salió una versión nueva del juego o del entorno, y advertencias.
- **Error** {colors.error} sobre {colors.error-container}: errores de formulario y mensajes de error. Es un rojo frambuesa, distinto del terracota, y siempre va con ícono y texto que dice qué hacer.
- **Info** usa el par de primary container.

Todos los pares de texto y fondo de este archivo cumplen 4.5:1 (WCAG AA).

## Typography

Tres familias, todas con licencia SIL Open Font License, servidas desde `static/` (sin pedirlas a Google Fonts) y con respaldo del sistema:

- **Source Serif 4** para leer: títulos, subtítulo, texto de la lección y el nombre EngiMods. Da calidez y autoridad de libro.
- **Plus Jakarta Sans** para la interfaz: navegación, botones, etiquetas, metadatos, formularios, consejos y notas. Es amable y redondeada, y separa "lo que lees" de "lo que usas".
- **JetBrains Mono** para código y versiones (`Juego 1.4 + Loader 0.9`), que siempre van en monoespaciada porque son datos exactos.

Escala:

- `title-lg` para el título de la página en escritorio y `title-md` en teléfono (menos de 640 px).
- `dek`, **en cursiva** y en {colors.ink-soft}, para el subtítulo de una frase debajo del título: explica por qué vale la pena, no qué contiene.
- `headline-md` para secciones dentro de la lección y `headline-sm` para títulos de tarjeta, la siguiente lección y el nombre del curso en el temario.
- `reading-lg` (20 px) para el texto de la lección en escritorio y `reading-md` (19 px) en teléfono. Las frases de acompañamiento ("para eso estamos") van en `reading-md` cursiva y {colors.ink-soft}.
- `body-md` y `body-sm` para texto de interfaz; `label-md` para botones y navegación; `label-sm` para chips y metadatos.
- `eyebrow` **en mayúsculas** para etiquetas de sección pequeñas ("AL TERMINAR PODRÁS", "EN ESTA LECCIÓN", nombres de módulo).
- `code-md` en bloques y `code-sm` en versiones, código en línea y números de lección.

## Layout

Pensado primero para 360 px; el escritorio se arma con tres zonas.

- **Escritorio (1024 px o más) dentro de un curso:** temario a la izquierda ({spacing.sidebar}, fondo {colors.surface-sunken}), lección al centro (máximo {spacing.reading-max}, unos 680 px) y, a la derecha, el índice "En esta lección" con la ficha de la lección ({spacing.aside}).
- **Entre 640 y 1023 px:** la columna derecha baja debajo del encabezado de la lección y el temario se pliega arriba.
- **Teléfono:** una sola columna con margen de {spacing.gutter}. El temario es un panel plegable arriba de la lección, la ficha se vuelve chips debajo del título y los botones de avance ocupan todo el ancho.
- **Fuera de un curso** (catálogo, detalle del curso, Mi panel, formularios): contenido centrado hasta 72 rem, sin temario.
- La barra de navegación mide {spacing.nav-height}: el nombre EngiMods a la izquierda, el avance del curso al centro cuando estás dentro de uno y los enlaces a la derecha.
- Escala de espacio de 4 en 4: {spacing.xs}, {spacing.sm}, {spacing.md}, {spacing.lg}, {spacing.xl} y {spacing.xxl}. Entre secciones de una lección, 48 px; alrededor de la lección, {spacing.xxl} arriba y 96 px abajo en escritorio.
- Todo lo que se toca mide al menos {spacing.touch-target}.

## Elevation & Depth

Plano, como el papel. La jerarquía se da con el contraste entre {colors.background}, {colors.surface-sunken} y {colors.surface}, con bordes {colors.divider} y con el tamaño de los títulos. No hay sombras. La lección actual del temario se marca con fondo blanco y un borde de 1 px, no con sombra. El anillo de foco es de 2 px de {colors.primary}, separado 2 px del elemento.

## Shapes

Suave y amable, sin llegar a infantil.

- {rounded.full} (píldora) en botones, chips, sellos de versión y avatar.
- {rounded.lg} en tarjetas, el cuadro "Al terminar podrás", consejos, mensajes y bloques de código.
- {rounded.md} en campos de formulario y elementos del temario; 10 px en los cuadritos numerados de lección.
- El sello de "Probado" es un círculo con borde de 2 px, girado -6°, como un sello de tinta.

## Components

- **Barra de navegación** (`nav-bar`): sobre el papel, con borde inferior {colors.divider}. `wordmark` EngiMods a la izquierda. Dentro de un curso, al centro: "Misión Cero · 2 de 9" y una `progress-bar`. A la derecha, "Juegos" y "Mi panel" o "Entrar". En teléfono, los enlaces van en un botón redondo de menú y la barra de avance se vuelve una línea de 3 px bajo la barra.
- **Encabezado de lección:** ruta en `label-sm` muted ("Módulo 1 · Fundamentos · Lección 3 de 9"), título, `dek` en cursiva, y a la derecha el `tested-stamp`. Debajo, entre dos divisores, la **línea de autor**: `avatar` con iniciales, "[Nombre del tutor]" y "Escribió y revisó esta lección el [fecha]", y un `chip` con la duración.
- **Sello de versión probada** (`tested-stamp`): la pieza más propia de EngiMods. Círculo verde con "PROBADO", una línea y las versiones en monoespaciada. Va junto al título de cada lección. En espacios chicos (tarjetas, listas, ficha) se usa la versión en píldora `badge-tested`. Variantes con palabras: `badge-revalidate` ("Pendiente de revalidar · Juego 1.5") y `badge-untested` ("Sin versión probada").
- **"Al terminar podrás"** (`outcomes-box`): tarjeta blanca al inicio de cada lección con 2 a 4 logros en verbo infinitivo ("Crear un repositorio para tu mod."). Sustituye al video: la lección empieza por lo que vas a lograr.
- **Texto de lección:** `reading-lg` en {colors.ink}, secciones en `headline-md` con `id` para el índice. Enlaces terracota y subrayados.
- **Nota al margen** (`margin-note`): "※ Si ya usas Git, puedes pasar a la siguiente sección." En sans pequeña y muted, con sangría. Para condiciones, atajos y aclaraciones; nunca para algo que el alumno deba hacer.
- **Consejo** (`callout-tip`): ícono de foco de línea, "**Consejo:**" y una o dos frases. Uno o dos por lección como máximo.
- **Bloque de código** (`code-block`): oscuro, con una cabecera (`code-block-header`) que dice "Terminal" o el nombre del archivo y un botón "Copiar". Desplazamiento horizontal propio: la página nunca se mueve a los lados.
- **Cierre de lección:** una frase de acompañamiento en cursiva con enlace al tutor, luego una tarjeta con "Siguiente lección", su título en `headline-sm` y el `button-primary` "Terminé esta lección · seguir". Debajo, un enlace discreto a la lección anterior.
- **Temario** (`sidebar`): nombre del curso en `headline-sm` y una frase de avance ("Vas muy bien: 2 lecciones completas"). Módulos en `eyebrow`. Cada lección es un renglón con su `lesson-tile` numerado (01, 02…) que lleva en la base una barra de 3 px con el avance de esa lección, el título y una línea muted ("Completada", "Estás aquí · 25 min"). La lección actual usa `lesson-tile-current` y `syllabus-item-current`.
- **En esta lección:** `eyebrow` y los enlaces a las secciones, con un borde izquierdo de 2 px: terracota en la sección actual y {colors.divider} en las demás. Debajo, la **ficha** en una tarjeta: "Probado con", "Necesitas" y "Entrega", como lista de definiciones. Cierra con "¿Algo no funciona? Avísanos".
- **Botón principal** (`button-primary`): píldora terracota con texto blanco, 48 px de alto. Uno por pantalla como máximo: la acción que la persona vino a hacer (seguir, pagar, enviar la entrega).
- **Botón secundario** (`button-secondary`): píldora blanca con borde {colors.outline} y texto terracota. **Botón discreto** (`button-quiet`): píldora {colors.surface-chip} para acciones menores (menú, copiar).
- **Chip** (`chip`): píldora {colors.surface-chip} para datos cortos: duración, requisitos, tipo de curso. No se toca, así que no lleva terracota.
- **Barra de avance** (`progress-bar`): riel {colors.progress-track} y relleno {colors.primary}, siempre con `role="progressbar"` y un texto que diga el avance ("2 de 9").
- **Campos de formulario** (`input-field`): blancos, con borde {colors.outline} de 1 px, esquinas {rounded.md} y etiqueta visible arriba en `label-md`. Texto a 16 px para que el teléfono no haga zoom. Con error, borde de 2 px y mensaje abajo en {colors.error} (`input-field-error`) que dice qué hacer.
- **Tarjeta** (`card`): blanca, con borde {colors.divider} y esquinas {rounded.lg}. Para un curso: etiqueta en `label-sm` muted (juego y tipo), título en `headline-sm`, una línea de metadatos o chips, avance si aplica y una acción.
- **Mensajes de Django** (`message-success`, `message-info`, `message-warning`, `message-error`): franja con el fondo claro de su estado arriba del contenido, con una palabra en negritas al inicio ("Listo.", "Aviso.", "No se pudo guardar.") y texto que se entiende sin depender del color.
- **Estado vacío:** tarjeta con una frase cálida que dice qué falta y qué hacer ("Aún no tienes cursos. Empieza con Misión Cero para crear tu primer mod.") y un `button-secondary`.

## Do's and Don'ts

- **Do** pon el sello de versión probada en cada lección, junto al título. Es la promesa de EngiMods.
- **Do** di quién escribió y revisó cada lección, y cuándo. La confianza tiene nombre.
- **Do** empieza cada lección con "Al terminar podrás" y termina con una frase de acompañamiento y la siguiente lección.
- **Do** escribe en español de México, directo, cálido y en segunda persona: "Envía tu entrega", "Si te atoras, es normal". Reconoce el avance sin exagerar ("Vas muy bien").
- **Do** pon las condiciones a la vista (notas ※, la ficha, chips), nunca en letra chica escondida.
- **Do** muestra el foco de teclado siempre y respeta `prefers-reduced-motion`. Las transiciones, si existen, duran 150 ms o menos.
- **Don't** satures: un botón principal por pantalla, uno o dos consejos por lección, nada de banners que compitan entre sí.
- **Don't** uses arte, capturas, logos ni colores de un juego en la interfaz. El juego aparece como dato, no como decoración.
- **Don't** agregues degradados, brillos, sombras, efectos de vidrio, emojis ni estética "gamer".
- **Don't** uses el terracota en texto que no se puede tocar ni en chips. Su significado es "esto es interactivo" o "este es tu avance".
- **Don't** comuniques un estado solo con color. El sello dice "Probado", "Pendiente de revalidar" o "Sin versión probada" con palabras.
- **Don't** prometas resultados ("domina", "conviértete en experto", "garantizado"). Te acompañamos a construir; no vendemos atajos.
- **Don't** pongas la lección dentro de una tarjeta: el texto va sobre el papel.
- **Don't** agregues modo oscuro por ahora. Se puede proponer después con sus propios valores.
