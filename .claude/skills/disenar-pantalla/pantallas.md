# Anatomía de las pantallas

Cada tipo de pantalla se arma con las mismas piezas, en el mismo orden. Los nombres entre comillas invertidas son componentes de `DESIGN.md`; las clases `em-*` son las de `referencia/engimods.css`. De arriba abajo, en teléfono; las notas de escritorio van al final de cada bloque.

## Estructura común

```
nav-bar          wordmark · [avance del curso, si estás dentro de uno] · enlaces
mensajes         message-* de Django, si hay
contenido        según el tipo de pantalla
pie              enlaces a términos y aviso de privacidad, en body-sm
```

- Fuera de un curso, el contenido se centra hasta `page-max` (72 rem) con margen de 16 px. `base.html` ya pone la barra, los mensajes, ese contenedor y el pie.
- Dentro de un curso (lección, entrega), el escritorio usa tres zonas: `sidebar` · lección · "En esta lección". Ver `referencia/leccion.html`.

## Lección (`courses:lesson_detail`)

La pantalla canónica. Es exactamente `referencia/leccion.html`.

1. **Temario plegable** (teléfono): un `<details>` con "Misión Cero · lección 3 de 9", "Vas muy bien: 2 completas" y "Temario". En escritorio es el `sidebar` fijo a la izquierda y siempre abierto (la referencia lo abre con un script de cinco líneas; sin JavaScript se sigue pudiendo abrir a mano).
2. **Ruta** en `label-sm` muted: "Módulo 1 · Fundamentos · Lección 3 de 9".
3. **Título** (`title-lg`, o `title-md` en teléfono) y **`dek`** en cursiva.
4. **`tested-stamp`** a la derecha del título (en teléfono, al lado de la línea de autor). Si la lección no tiene versión probada: `badge-untested`. Si está pendiente de revalidar: `badge-revalidate` arriba del título, además del sello de la versión con la que sí se probó.
5. **Línea de autor**, entre dos `divider`: `avatar`, "[Nombre del tutor]", "Escribió y revisó esta lección el [fecha]" y `chip` "25 min de lectura".
6. **Ficha**: en escritorio va en la columna derecha (Probado con, Necesitas, Entrega). En teléfono son `chip`s debajo de la línea de autor.
7. **`outcomes-box`** "Al terminar podrás", con 2 a 4 logros.
8. **Contenido** (Markdown sanitizado): `reading-lg`, secciones `headline-md` con `id`, `code-block` con cabecera y "Copiar", `margin-note` ※, como máximo dos `callout-tip`.
9. **Frase de acompañamiento** en cursiva con enlace al tutor.
10. **Cierre**: tarjeta "Siguiente lección" con `button-primary` "Terminé esta lección · seguir" y, abajo, el enlace "← [lección anterior]". En teléfono, el botón ocupa todo el ancho.

## Landing (`core:home`)

La puerta de entrada. Dice qué es EngiMods y lleva a Misión Cero. Es `templates/core/home.html`.

1. **Encabezado**, en una columna de `reading-max`: `eyebrow` ("Academia de modding en español"), título y `dek` en cursiva. Sin imagen, sin degradado y sin arte de un juego.
2. **Llamados:** `button-primary` hacia la práctica corta. Si solo hay una, lleva a su página ("Empieza con [título]"); si hay varias, a la lista de cursos. `button-secondary` hacia el curso por grupos ("Conoce el grupo piloto"). Si no hay curso por grupos publicado, una línea muted que lo dice. En teléfono, los botones ocupan todo el ancho.
3. **Cómo aprendes aquí:** cuatro `card`s (una columna en teléfono, dos desde 640 px) con la propuesta de valor: ruta en español, ejercicios pequeños, versión comprobada y revisión de lo que construyes. El plazo de revisión sale de settings (`REVIEW_DEADLINE_HOURS`), no se escribe a mano.
4. **Cursos** (`id="cursos"`): primero las prácticas cortas. Cada `card`: juego y tipo en `label-sm` muted, título `headline-sm`, descripción corta, `chip`s (nivel, duración, acceso), `badge-tested` con la prueba más reciente de sus lecciones publicadas (o `badge-untested`), precio y `button-secondary` "Ver el curso".
5. **Juegos:** `card` por juego activo con su nombre como dato (sin logo), descripción, `chip` en monoespaciada con la versión actual y `chip` con sus cursos publicados. El nombre enlaza a la página del juego.
6. **Estados vacíos:** sin cursos, una tarjeta punteada que lo dice; sin juegos, una frase.

## Detalle del curso (`courses:course_detail`)

Es donde se decide el pago: todo lo que da confianza va aquí, a la vista.

1. Etiqueta `label-sm` muted: "[Juego] · Práctica autoguiada" o "Curso de seis semanas · por grupos".
2. Título `title-lg` y `dek` con lo que vas a construir (un logro, no una lista de temas).
3. `badge-tested` con la versión con la que se probó el curso.
4. **"Al terminar podrás"** (`outcomes-box`).
5. **Temario**: un `card` por módulo, con sus lecciones numeradas (`lesson-tile` sin avance) y su duración.
6. **Quién te acompaña**: `avatar`, nombre y una línea sobre el tutor o el equipo. Si no hay dato, el marcador `[Nombre del tutor]`; no inventes biografías.
7. **Caja de inscripción** (en escritorio, columna derecha; en teléfono, después del temario y repetida como barra al final): precio en `title-md` con "MXN", lista de lo que incluye con íconos verdes (acceso por [DÍAS] días, revisión en 24 horas si aplica, requisitos), `button-primary` "Inscribirme y pagar" y `margin-note` con el enlace a términos y política de devolución.
8. **Preguntas frecuentes** si existen, como lista de `<details>`.

## Confirmar y pagar

Inspirada en la pantalla de confirmación japonesa: antes de cobrar, la persona ve todo lo que va a pasar.

1. Pasos visibles: "1 Revisa · 2 Paga · 3 Empieza", con el paso actual en `ink` y los demás en muted.
2. Resumen en `card`: curso, precio, acceso por [DÍAS] días desde el pago, y qué recibes por correo.
3. `margin-note` con la política de devolución resumida y el enlace al texto completo.
4. Casilla con `<label>` para aceptar los términos.
5. `button-primary` "Pagar con Stripe" y `button-secondary` "Volver al curso".

## Mi panel (`enrollments:my_courses`)

1. `message-success` si acaba de pagar ("**Pago confirmado.** Ya tienes acceso a Misión Cero.").
2. Título `title-md` "Mis cursos" y una línea muted.
3. Rejilla de `card`s (una columna en teléfono, `repeat(auto-fill, minmax(min(100%, 320px), 1fr))` en escritorio). Cada tarjeta: etiqueta, título `headline-sm`, `progress-bar` con "3 de 9 lecciones", "Acceso hasta el [fecha]", `badge-revalidate` si hay lecciones pendientes, y `button-primary` "Continuar: [lección]". Solo la primera tarjeta lleva botón principal; las demás, `button-secondary`.
4. **Estado vacío**: `card` con "Aún no tienes cursos. Empieza con Misión Cero para crear tu primer mod." y `button-secondary` "Ver Misión Cero".

## Catálogo de juegos y detalle de juego (`catalog:*`)

1. Título `title-md` y `dek` corto.
2. Rejilla de `card`s: nombre del juego como dato en `headline-sm` (sin logo ni arte del juego), versiones soportadas en `badge-tested`, entornos de modding como `chip`s y el número de cursos.
3. En el detalle: tabla de versiones (versión del juego, entorno, fecha de prueba, estado con `badge-*`) dentro de un contenedor con desplazamiento horizontal propio en teléfono.

## Formularios (entrega, registro, datos)

1. Título y una línea que diga para qué es y cuánto tarda ("Tu tutor lo revisa en menos de 24 horas.").
2. Un campo por renglón: `<label>` en `label-md`, `input-field` de 48 px, texto de ayuda en `body-sm` muted debajo.
3. Error: `input-field-error` debajo del campo y un `message-error` arriba del formulario que resume qué corregir. Los mensajes dicen qué hacer.
4. Un `button-primary` con el verbo de la acción ("Enviar mi entrega"), alineado a la izquierda en escritorio y a todo el ancho en teléfono.

## Vista del tutor

El tutor trabaja en pantallas propias, no en el admin (`docs/arquitectura.md`). Usa la estructura común sin `sidebar`, con la misma identidad: lista de entregas como tabla o `card`s con estado (`badge-*` con palabras: "Por revisar", "Revisada"), plazo restante en `chip` y `button-primary` "Revisar" solo en la más urgente.

## Textos legales y páginas de lectura

Columna de lectura (`reading-max`), título `title-md`, fecha de vigencia en muted, texto en `reading-md`. Sin tarjetas ni botones principales.

## Errores 404 y 500

Columna centrada: `title-md` ("No encontramos esta página"), una frase que diga qué hacer y un `button-secondary` a Mi panel o al inicio. Sin ilustraciones de un juego.
