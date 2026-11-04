---
name: disenar-pantalla
description: Diseña, maqueta o revisa una pantalla de EngiMods con su identidad visual (DESIGN.md) para que se vea igual que las demás. Úsala antes de crear o cambiar una plantilla en templates/, un boceto o una maqueta; cuando la persona pida "diseña la pantalla de X", "dale estilo a", "que se vea como la lección" o "revisa si esto sigue el diseño"; y al revisar un PR que toque pantallas.
---

# Diseñar una pantalla de EngiMods

La identidad visual vive en `DESIGN.md`, en la raíz. Esta skill explica cómo aplicarla a una pantalla nueva sin inventar nada: qué leer, qué anatomía usar, cómo escribir los textos y cómo comprobar el resultado.

## Antes de empezar

1. **Revisa el estado.** `DESIGN.md` y el ADR 0002 (`docs/decisiones/0002-estilos-frontend.md`) dicen si la propuesta ya se aceptó y con qué se implementan los estilos (Tailwind, CSS propio u otro).
   - **Propuesta, sin aceptar:** puedes hacer bocetos, maquetas y propuestas con esta skill. En las plantillas de una historia, escribe HTML semántico con la anatomía de `pantallas.md`, para que el estilo se aplique después sin reescribir. No agregues CSS, dependencias ni fuentes a `static/` por tu cuenta: eso es de EM-004.
   - **Aceptada:** sigue `DESIGN.md` en cada pantalla, con el enfoque que diga el ADR.
2. **Lee `DESIGN.md` completo.** Los valores (YAML) mandan; el texto dice cuándo usar cada uno. No copies valores de memoria ni de bocetos viejos.
3. **Abre la referencia en el navegador:** `referencia/leccion.html` (la lección completa, escritorio y teléfono) y `referencia/componentes.html` (cada componente con sus estados). Son la forma canónica; si tu pantalla se ve distinta, revisa por qué.
4. **Ubica tu pantalla en `pantallas.md`** y usa su anatomía. Si no aparece, toma la más parecida y dilo en el PR.

## Al construir

- **Valores, no números sueltos.** Todo color, tamaño, espacio y esquina sale de un token de `DESIGN.md`. Si necesitas uno que no existe, no lo inventes en la plantilla: propón agregarlo a `DESIGN.md` en el PR.
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

Si cambiaste `DESIGN.md` o `referencia/engimods.css`, corre `uv run python .claude/skills/disenar-pantalla/revisar_tokens.py`: compara los colores, esquinas y espacios de los dos archivos y falla si no coinciden. Si existe el linter oficial (`npx @google/design.md lint DESIGN.md`), córrelo también.

## Al revisar un PR con pantallas

Usa la lista anterior. Reporta cada diferencia con el token o la regla de `DESIGN.md` que no se cumple y, si se puede, la línea de la plantilla. Una pantalla que funciona pero se ve distinta no está terminada: la Definition of Done pide que "se vea bien en teléfono" y, una vez aceptado el ADR 0002, que siga `DESIGN.md`.
