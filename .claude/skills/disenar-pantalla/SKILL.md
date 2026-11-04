---
name: disenar-pantalla
description: Diseña, maqueta o revisa una pantalla de EngiMods con su identidad visual (DESIGN.md) para que se vea igual que las demás. Úsala antes de crear o cambiar una plantilla en templates/, un boceto o una maqueta; cuando la persona pida "diseña la pantalla de X", "dale estilo a", "que se vea como la lección" o "revisa si esto sigue el diseño"; y al revisar un PR que toque pantallas.
---

# Diseñar una pantalla de EngiMods

La identidad visual vive en `DESIGN.md`, en la raíz. Esta skill explica cómo aplicarla a una pantalla nueva sin inventar nada: qué leer, qué anatomía usar, cómo escribir los textos y cómo comprobar el resultado.

## Antes de empezar

1. **Revisa el estado.** El ADR 0002 (`docs/decisiones/0002-estilos-frontend.md`) se aceptó el 2026-11-04: toda pantalla sigue `DESIGN.md` y los estilos se escriben con clases de Tailwind (ver "Con Tailwind", abajo). Si un ADR posterior lo reemplaza, sigue ese.
2. **Lee `DESIGN.md` completo.** Los valores (YAML) mandan; el texto dice cuándo usar cada uno. No copies valores de memoria ni de bocetos viejos.
3. **Abre la referencia en el navegador:** `referencia/leccion.html` (la lección completa, escritorio y teléfono) y `referencia/componentes.html` (cada componente con sus estados). Son la forma canónica; si tu pantalla se ve distinta, revisa por qué.
4. **Ubica tu pantalla en `pantallas.md`** y usa su anatomía. Si no aparece, toma la más parecida y dilo en el PR.

## Al construir

- **Valores, no números sueltos.** Todo color, tamaño, espacio y esquina sale de un token de `DESIGN.md`. Si necesitas uno que no existe, no lo inventes en la plantilla: propón agregarlo a `DESIGN.md` en el PR.
- **Con Tailwind.** El bloque `@theme` de `assets/tailwind.css` copia los valores de `DESIGN.md`, así que cada token es una clase:

  | En `DESIGN.md` | En la plantilla |
  |---|---|
  | `colors.primary`, `colors.ink-muted` | `bg-primary`, `text-ink-muted`, `border-divider` |
  | `typography.title-lg`, `typography.label-sm` | `font-serif text-title-lg`, `font-sans text-label-sm`: la familia va aparte, según el token |
  | `rounded.lg` | `rounded-lg` |
  | `spacing.md`, `spacing.reading-max` | `p-md`, `gap-md`, `mt-lg`, `max-w-reading-max`, `min-h-touch-target` |
  | `button-primary`, `button-secondary`, `button-quiet` | clases con el mismo nombre, en `<button>` o en `<a>` |

  La escala numérica de Tailwind (`px-5` = 20 px) queda para medidas de un componente que no tienen token. Los colores, tamaños de texto, esquinas y sombras propios de Tailwind no existen (`bg-blue-500` o `text-sm` no generan nada). `base.html` ya pone la barra, los mensajes, el contenedor y el pie, y el HTML sin clases (títulos, párrafos, listas, tablas, formularios, código, botones secundarios) ya sigue `DESIGN.md`: agrega clases solo para lo que la pantalla necesita. Para verla, `uv run python manage.py tailwind runserver`.
- **Una sola pieza nueva a la vez.** Si la pantalla necesita un componente que no está en `DESIGN.md`, arma con los existentes. Si de verdad hace falta uno nuevo, descríbelo en `DESIGN.md` (YAML y texto) y agrégalo a `referencia/componentes.html` en el mismo cambio.
- **Teléfono primero.** Diseña a 360 px y luego amplía. Revisa 360, 768 y 1280 px.
- **HTML real y accesible:** `<button>`, `<a href>`, `<label>` unido a su `<input>`, `aria-current="page"` en la ubicación actual, `role="progressbar"` con `aria-valuenow`, `aria-label` en botones con solo ícono, íconos decorativos con `aria-hidden="true"`. Nada de `onclick` en un `<div>`.
- **Íconos:** SVG de línea, de 1.8 a 2 px de trazo, del color del texto (`currentColor`). Sin emojis.
- **Textos visibles** con `{% translate %}` o `gettext_lazy` (`AGENTS.md`, sección 6). Datos de negocio (precios, días, cupos) desde la base o settings; en bocetos, como marcadores `[PRECIO]`, `[DÍAS]`, `[CUPO]`, `[Nombre del tutor]`.
- **Ningún juego concreto** en la interfaz: el juego y su versión son datos (`Juego 1.4 + Loader 0.9` en ejemplos).

## Voz y textos

La voz es la mitad de la identidad. EngiMods es cálido, sabe lo que enseña y es humilde.

| Haz | Evita |
|---|---|
| "Envía tu entrega" (segunda persona, imperativo amable) | "Enviar entrega", "El usuario debe enviar…" |
| "Al terminar podrás crear un repositorio para tu mod." | "En esta lección se verán los temas: Git, commits…" |
| "Si algo no sale a la primera, es parte de aprender." | "¡Error! Algo salió mal." |
| "Vas muy bien: 2 lecciones completas." | "¡¡Increíble!! 🔥 Eres un crack" |
| "Tu tutor lo revisa en menos de 24 horas." | "Revisión ultra rápida garantizada" |
| "※ Si ya usas Git, puedes pasar a la siguiente sección." | Condiciones escondidas en letra chica |
| "Escribe un correo completo, por ejemplo nombre@dominio.mx." | "Correo inválido." |

Reglas: español de México; frases cortas; un dato exacto vale más que un adjetivo; nunca prometas resultados ("domina", "experto", "garantizado"); los errores dicen qué hacer.

## Comprobar antes de entregar

- [ ] La pantalla sigue su anatomía de `pantallas.md`.
- [ ] Todos los colores, tipografías, espacios y esquinas son tokens de `DESIGN.md`.
- [ ] Un solo `button-primary` por pantalla.
- [ ] El terracota (`primary`) solo está en lo que se toca y en barras de avance.
- [ ] Si la pantalla muestra una lección o un recurso, tiene su sello de versión (`tested-stamp` o `badge-*`) con palabras.
- [ ] A 360 px no hay desplazamiento horizontal de la página; los bloques de código se desplazan solos.
- [ ] Todo lo que se toca mide al menos 44 px; el foco de teclado se ve.
- [ ] Contraste de 4.5:1 en texto y 3:1 en bordes de campos (los pares de `DESIGN.md` ya cumplen; si combinas otros, mídelo).
- [ ] Los textos siguen la tabla de voz y están en español de México.
- [ ] Hay estado vacío, de error y de carga cuando aplica.
- [ ] Sin sombras, degradados, emojis ni arte de un juego.

Si cambiaste un valor de `DESIGN.md`, cámbialo también en `assets/tailwind.css` y en `referencia/engimods.css`. `core/tests/test_design_tokens.py` (en `pytest`) compara `DESIGN.md` con el tema de Tailwind, y `uv run python .claude/skills/disenar-pantalla/revisar_tokens.py` lo compara con la hoja de referencia. Si existe el linter oficial (`npx @google/design.md lint DESIGN.md`), córrelo también.

## Al revisar un PR con pantallas

Usa la lista anterior. Reporta cada diferencia con el token o la regla de `DESIGN.md` que no se cumple y, si se puede, la línea de la plantilla. Una pantalla que funciona pero se ve distinta no está terminada: la Definition of Done pide que siga `DESIGN.md` y se vea bien en teléfono.
