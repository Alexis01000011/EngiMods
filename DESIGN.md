---
version: alpha
name: EngiMods
description: Academia en línea para crear mods de videojuegos con ingeniería de software. Se ve como la documentación oficial de un kit de desarrollo de mods.
colors:
  primary: "#2F45C5"
  primary-hover: "#2436A0"
  on-primary: "#FFFFFF"
  primary-container: "#E8ECFB"
  ink: "#1B2430"
  ink-muted: "#55606E"
  background: "#F6F7F9"
  surface: "#FFFFFF"
  surface-code: "#EEF1F5"
  divider: "#D5DAE1"
  outline: "#7D8796"
  tested: "#17663F"
  tested-container: "#E3F3EA"
  revalidate: "#7A4F00"
  revalidate-container: "#FFF1CC"
  error: "#B3261E"
  error-container: "#FCE8E6"
typography:
  headline-lg:
    fontFamily: system-ui, sans-serif
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: -0.01em
  headline-md:
    fontFamily: system-ui, sans-serif
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.3
  headline-sm:
    fontFamily: system-ui, sans-serif
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.4
  body-md:
    fontFamily: system-ui, sans-serif
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: system-ui, sans-serif
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: system-ui, sans-serif
    fontSize: 0.9375rem
    fontWeight: 600
    lineHeight: 1.25
  code-md:
    fontFamily: ui-monospace, monospace
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.6
  code-sm:
    fontFamily: ui-monospace, monospace
    fontSize: 0.8125rem
    fontWeight: 500
    lineHeight: 1.3
rounded:
  sm: 4px
  md: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  gutter: 16px
  touch-target: 44px
  content-max: 45rem
  page-max: 72rem
  sidebar: 16rem
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
  nav-bar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label-md}"
    height: 56px
    padding: "{spacing.md}"
  link:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
  text-muted:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.body-sm}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 12px
    height: "{spacing.touch-target}"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 12px
    height: "{spacing.touch-target}"
  input-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px
    height: "{spacing.touch-target}"
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
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  divider:
    backgroundColor: "{colors.divider}"
    height: 1px
  code-block:
    backgroundColor: "{colors.surface-code}"
    textColor: "{colors.ink}"
    typography: "{typography.code-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  badge-tested:
    backgroundColor: "{colors.tested-container}"
    textColor: "{colors.tested}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.sm}"
    padding: 4px
  badge-revalidate:
    backgroundColor: "{colors.revalidate-container}"
    textColor: "{colors.revalidate}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.sm}"
    padding: 4px
  badge-untested:
    backgroundColor: "{colors.surface-code}"
    textColor: "{colors.ink-muted}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.sm}"
    padding: 4px
  message-success:
    backgroundColor: "{colors.tested-container}"
    textColor: "{colors.tested}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  message-info:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  message-error:
    backgroundColor: "{colors.error-container}"
    textColor: "{colors.error}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
---

# DESIGN.md de EngiMods

Estado: **propuesta**, ligada al [ADR 0002](docs/decisiones/0002-estilos-frontend.md). Mientras el equipo no la acepte, no es obligatoria para EM-004 ni para ninguna pantalla.

Este archivo sigue el formato [DESIGN.md](https://github.com/google-labs-code/design.md) de Google Labs (versión `alpha`): los valores exactos están arriba, en YAML, y el texto explica cuándo y por qué se usan. Los títulos de sección van en inglés porque así los reconoce el formato; el contenido va en español. Si un valor y el texto no coinciden, manda el valor y se corrige el texto.

## Overview

EngiMods se ve como **la documentación oficial de un kit de desarrollo de mods**: escrita por ingenieros para alguien que va a abrir su editor en cinco minutos. La página trabaja; no vende. Texto a tamaño de lectura, bloques de código que se copian sin pelear y la versión probada siempre a la vista, como la versión impresa en la portada de un manual.

Quien la lee es hispanohablante, casi siempre en México, sabe programar lo básico y muchas veces entra desde el teléfono. Debe sentir que le hablan en serio, como a alguien del oficio, y que lo que lee funciona con la versión del juego que tiene instalada.

EngiMods enseña a hacer mods de varios juegos. La interfaz es la misma para todos: ningún juego le pone su color, su tipografía ni su arte a la plataforma.

## Colors

Un sistema de tinta sobre papel con un solo acento.

- **Background** {colors.background}: el gris casi blanco de la página. Separa el contenido del borde de la pantalla sin llamar la atención.
- **Surface** {colors.surface}: blanco puro para lo que se lee: la lección, las tarjetas y los formularios.
- **Ink** {colors.ink}: todo el texto y los títulos. Azul muy oscuro, nunca negro puro.
- **Ink muted** {colors.ink-muted}: fechas, metadatos, texto de ayuda. Nunca para el texto principal de una lección.
- **Primary** {colors.primary}: índigo, el único acento. Es el color de lo que se puede tocar: enlaces, botones principales y el anillo de foco. Si algo es índigo, se puede usar. **Primary hover** {colors.primary-hover} es su estado al pasar el puntero o presionar.
- **Primary container** {colors.primary-container}: fondo de avisos informativos.
- **Surface code** {colors.surface-code}: fondo de los bloques de código y de las etiquetas neutras.
- **Divider** {colors.divider}: separadores decorativos. **Outline** {colors.outline}: borde de campos de formulario, con contraste suficiente para verse.

Tres colores de estado, siempre en pareja de texto y fondo claro:

- **Tested** {colors.tested} sobre {colors.tested-container}: "Probado con" y mensajes de éxito.
- **Revalidate** {colors.revalidate} sobre {colors.revalidate-container}: contenido pendiente de revalidar porque salió una versión nueva del juego o del entorno.
- **Error** {colors.error} sobre {colors.error-container}: errores de formulario y mensajes de error.

## Typography

Fuentes del sistema: `system-ui` para el texto y `ui-monospace` para código y versiones. No se descargan fuentes web, así que no hay peticiones a terceros, ni costo, ni espera en datos móviles. Cada persona ve la letra de su propio sistema, como en la documentación de muchas herramientas de desarrollo.

- **Títulos:** `headline-lg` para el título de la página, `headline-md` para secciones y `headline-sm` para subsecciones y títulos de módulo. Los saltos de tamaño son modestos: es un manual, no una revista.
- **Texto:** `body-md` a 16 px con interlineado de 1.6 para leer lecciones largas. `body-sm` para metadatos y texto de ayuda, nunca para párrafos de lección.
- **Etiquetas:** `label-md` para botones y navegación.
- **Código:** `code-md` dentro de bloques y en línea. `code-sm` para las versiones (`Juego 1.4 + Loader 0.9`), que siempre van en monoespaciada porque son datos exactos, no prosa.

## Layout

Una columna, pensada primero para 360 px de ancho.

- Margen lateral de {spacing.gutter} en teléfono. El texto de una lección nunca pasa de {spacing.content-max} de ancho, aunque la pantalla sea grande, para que las líneas se puedan leer.
- En escritorio el contenido se centra hasta {spacing.page-max}. Dentro de un curso, a partir de 1024 px, el temario pasa a una barra lateral de {spacing.sidebar} a la izquierda, como el índice de una documentación. En teléfono, el temario va arriba de la lección y se puede plegar.
- La escala de espacio es de 4 en 4: {spacing.xs}, {spacing.sm}, {spacing.md}, {spacing.lg}, {spacing.xl} y {spacing.xxl}. Entre secciones de una página, {spacing.xl}; entre párrafos, el margen natural del texto.
- Todo lo que se toca mide al menos {spacing.touch-target} de alto.

## Elevation & Depth

Plano. La jerarquía se da con el contraste entre {colors.background} y {colors.surface}, con bordes y con el tamaño de los títulos, no con sombras. No hay sombras, ni siquiera en tarjetas. La única capa que destaca es el anillo de foco: 2 px de {colors.primary} separado 2 px del elemento.

## Shapes

Esquinas apenas suavizadas. {rounded.sm} en botones, campos, etiquetas y mensajes; {rounded.md} en tarjetas y bloques de código. No hay formas de píldora ni círculos, salvo un avatar si algún día existe.

## Components

- **Barra de navegación** (`nav-bar`): blanca, con un borde inferior {colors.divider}. Tiene el nombre EngiMods a la izquierda y, a la derecha, "Mi panel" o "Entrar". En teléfono, los enlaces se pliegan en un botón "Menú".
- **Botón principal** (`button-primary`): índigo con texto blanco. Hay uno por pantalla como máximo: es la acción que la persona vino a hacer (pagar, enviar la entrega, guardar).
- **Botón secundario** (`button-secondary`): blanco con texto índigo y borde {colors.outline}. Para todo lo demás.
- **Enlaces** (`link`): índigo y subrayados dentro de la lección. En la navegación pueden ir sin subrayado.
- **Campos de formulario** (`input-field`): blancos, con borde {colors.outline} de 1 px y etiqueta visible arriba (nunca solo el texto de ejemplo). El texto va a 16 px para que el teléfono no haga zoom. Con error, el borde y el mensaje de abajo van en {colors.error} (`input-field-error`), y el mensaje dice qué hacer, no solo qué falló.
- **Tarjeta** (`card`): blanca, con borde {colors.divider}, para un curso en el panel o en el catálogo. Lleva el título, el juego, el tipo y una línea de metadatos en {colors.ink-muted}.
- **Bloque de código** (`code-block`): fondo {colors.surface-code} y desplazamiento horizontal propio. Nunca hace que toda la página se desplace a los lados.
- **Sello de versión probada** (`badge-tested`): la pieza más propia de EngiMods. En monoespaciada, verde, con el texto `Probado con <juego> <versión> + <entorno> <versión>`. Va justo debajo del título de cada lección. Sus variantes:
  - `badge-revalidate`: ámbar, cuando el contenido está pendiente de revalidar.
  - `badge-untested`: gris, cuando la lección no tiene versión probada registrada.
- **Mensajes de Django** (`message-success`, `message-info`, `message-error`): franja con el fondo claro de su estado arriba del contenido, con texto que se lee completo sin depender del color.

## Do's and Don'ts

- **Do** pon el sello de versión probada en cada lección, debajo del título y antes del contenido. Es la promesa de EngiMods.
- **Do** escribe los textos en español de México, directos y en segunda persona: "Envía tu entrega", no "Enviar entrega".
- **Do** deja que la página termine. Una lección corta que acaba a media pantalla está bien.
- **Do** muestra el foco de teclado siempre, y respeta `prefers-reduced-motion`. Las transiciones, si existen, duran 150 ms o menos.
- **Don't** uses arte, capturas, logos ni colores de un juego en la interfaz. EngiMods es de varios juegos; el juego aparece como dato, no como decoración.
- **Don't** agregues banners de héroe, degradados, brillos, sombras, efectos de vidrio ni estética "gamer". Esto es un manual.
- **Don't** uses el índigo en texto que no se puede tocar. Su significado es "esto es interactivo".
- **Don't** comuniques un estado solo con color. El sello dice "Probado con", "Pendiente de revalidar" o "Sin versión probada" con palabras.
- **Don't** agregues modo oscuro por ahora. Se puede proponer después con sus propios valores.
