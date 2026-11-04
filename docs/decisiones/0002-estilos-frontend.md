# 0002. Estilos del frontend

- Estado: Aceptada
- Fecha: 2026-11-03 (actualizada y aceptada el 2026-11-04)
- Historia: EM-004

## Contexto

La entrega de semestre requiere páginas de Django, navegación y mensajes que se
puedan usar a 360 px. Son tres personas, el presupuesto total del piloto es
MXN 1,500 y queda alrededor de un mes. El ADR 0001 mantiene plantillas del
servidor. No hay un enfoque de estilos elegido ni una cadena de compilación CSS.

Ya hay pantallas hechas sin estilos (detalle del curso, panel del alumno, lección
y términos), y casi todo el código lo escriben agentes. Hace falta decidir dos
cosas: con qué se implementan los estilos y cómo se describe la identidad visual
para que personas y agentes produzcan pantallas coherentes entre sí.

## Opciones consideradas

Fuentes consultadas el 2026-11-03 y, para Tailwind y DESIGN.md, el 2026-11-04.
Los costos siguientes son de herramientas; el trabajo de implementación y
mantenimiento no está monetizado.

| Opción | Costo mensual de herramienta | Configuración y compatibilidad | Ventajas y límites |
|---|---|---|---|
| CSS propio pequeño | MXN 0 / USD 0 | Un archivo en `static/`, incluido por `base.html`; sin efecto en PostgreSQL | Pocas piezas y sin compilación. El equipo debe diseñar y mantener formularios, estados, foco y navegación adaptable. |
| Bootstrap | MXN 0 / USD 0 por el paquete MIT | CSS distribuido por el proyecto; JavaScript solo para componentes que lo necesiten. Compatible con plantillas Django | Componentes y rejilla disponibles; hay que adaptar la apariencia y comprobar accesibilidad. Conservar avisos de licencia. |
| Tailwind CSS | MXN 0 / USD 0 por el paquete MIT | Se compila a un archivo estático con el CLI independiente, sin Node. La versión más reciente es la 4.3.4 (2026-11-02), con binarios para Linux, macOS y Windows x64. Compatible con plantillas Django | Facilita componer estilos con utilidades. Añade un paso reproducible de compilación y detección de clases en plantillas. |

Para integrar Tailwind con Django sin Node hay dos caminos verificados:

- **`django-tailwind-cli`** 4.8.2 (2026-10-27, licencia MIT). Declara soporte
  para Django 4.2, 5.2, 6.0 y 6.1, y para Windows, macOS y Linux. Descarga el
  CLI de las versiones publicadas de Tailwind en GitHub y agrega
  `manage.py tailwind build`, `tailwind watch` y `tailwind runserver`, además
  de la etiqueta `{% tailwind_css %}`. Por omisión usa la versión `latest` del
  CLI; se fija con `TAILWIND_CLI_VERSION`. Su documentación no menciona
  verificación de sumas de comprobación del binario descargado.
- **Descargar el CLI a mano** (o con `pytailwindcss` 0.4.2, que lo instala como
  paquete de Python) y correrlo con un script. Evita una dependencia, pero cada
  persona y cada entorno tiene que obtener el binario correcto para su sistema.

Además del enfoque, se consideró **DESIGN.md**, un formato abierto de Google
Labs (licencia Apache 2.0, versión `alpha`, CLI `@google/design.md` 0.4.0 del
2026-07-27). Es un archivo Markdown en la raíz del repositorio. Lleva los
valores del sistema de diseño (colores, tipografía, espacio, esquinas y
componentes) en YAML y un texto que explica cuándo usar cada uno, para que los
agentes de código lo lean antes de crear una pantalla. No depende del enfoque
CSS: sus valores se pueden volver variables de CSS propio, y su CLI exporta
directamente un bloque `@theme` de Tailwind v4. El CLI requiere Node, pero solo
para revisar el archivo o exportarlo, no para usar el sitio.

Fuentes: [inicio de Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/),
[licencia de Bootstrap](https://getbootstrap.com/docs/5.3/about/license/),
[Tailwind CLI](https://tailwindcss.com/docs/installation/tailwind-cli),
[versiones de Tailwind](https://github.com/tailwindlabs/tailwindcss/releases),
[licencia de Tailwind](https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE),
[django-tailwind-cli en PyPI](https://pypi.org/project/django-tailwind-cli/),
[ajustes de django-tailwind-cli](https://django-tailwind-cli.readthedocs.io/latest/settings.html),
[pytailwindcss en PyPI](https://pypi.org/project/pytailwindcss/) y
[DESIGN.md](https://github.com/google-labs-code/design.md).
No se incluyen plantillas, temas ni componentes comerciales.

Las tres alternativas permiten implementar EM-004 y dar una base a las páginas
posteriores. Ninguna afecta los modelos ni exige frontend separado. Cambiar CSS
propio por una biblioteca requeriría adaptar clases; cambiar Bootstrap por
Tailwind exigiría revisar más marcado. Esto es una valoración de mantenimiento,
no una medición de horas del equipo.

## Decisión

**Aceptada por el equipo el 2026-11-04: Tailwind CSS v4 con `django-tailwind-cli`,
la identidad visual de `DESIGN.md` y las fuentes servidas desde `static/`.** Alexis
la propuso ese mismo día; el equipo confirmó el enfoque, la identidad y las fuentes.

- `DESIGN.md` describe la identidad visual: la de un buen libro de texto, cálido y
  bien hecho, con la estructura de una documentación técnica: papel crema, lectura
  con serifa, un solo acento terracota para lo que se toca, el sello "Probado" junto
  a cada lección y quién la escribió y revisó. Sale de una exploración de tres
  direcciones (libro de texto, documentación y ruta de aprendizaje) que Alexis
  combinó. Pasa el linter oficial (`@google/design.md` 0.4.0) sin errores ni
  advertencias.
- Las tres familias tienen licencia SIL OFL (Source Serif 4, Plus Jakarta Sans y
  JetBrains Mono) y se sirven desde `static/fonts/`, no desde Google Fonts, para no
  mandar datos de los visitantes a terceros (ver el aviso de privacidad, EM-033).
  Son las versiones variables con el subconjunto latino de Fontsource (5.3.x):
  cuatro archivos `woff2` (serifa normal y cursiva, sans y mono) que suman 170 KB.
  El navegador solo descarga los que usa la página.
- La skill `disenar-pantalla` (`.claude/skills/disenar-pantalla/`) explica cómo
  aplicar `DESIGN.md` a cualquier pantalla y trae una lección y una galería de
  componentes de referencia.
- Tailwind convierte esos valores en clases que se usan directamente en las
  plantillas. Así, cada pantalla aplica el mismo sistema sin que alguien tenga
  que mantener a mano una hoja de estilos compartida.
- `django-tailwind-cli` evita Node, funciona en Windows y en Arch, y deja la
  compilación dentro de `manage.py`.

CSS propio era la opción con menos piezas, y `DESIGN.md` serviría igual con él. Lo
que cambió la balanza es que hay varias personas y agentes creando pantallas en
paralelo: con utilidades, el sistema queda en las clases y no en reglas CSS que se
pueden duplicar o contradecir.

Esta decisión no sustituye la revisión visual de cada pantalla.

## Consecuencias

EM-004 lo implementa así:

- Agrega `django-tailwind-cli` con `uv add` y fija `TAILWIND_CLI_VERSION` en
  `4.3.4`, no en `latest`. La suma SHA-256 del binario para Linux x64 coincidió con
  la que publica Tailwind en esa versión (revisado el 2026-11-04).
- El CSS fuente vive en `assets/tailwind.css`, fuera de `static/`. Su bloque
  `@theme` copia los valores de `DESIGN.md` y borra los de Tailwind (colores,
  fuentes, tamaños de texto, esquinas y sombras), así que solo existen las clases
  del sistema. `core/tests/test_design_tokens.py` falla si el tema y `DESIGN.md` no
  coinciden. Git ignora `.django_tailwind_cli/` y el CSS compilado.
- `base.html` trae navegación, pie y mensajes, y el CSS da estilo al HTML semántico
  sin clases, para que las pantallas que ya existían sigan legibles. Se revisó a
  360 y 1280 px, con teclado.
- `AGENTS.md` dice que las pantallas siguen `DESIGN.md`.

También cambia el trabajo diario:

- Para ver los estilos en desarrollo hay que correr
  `uv run python manage.py tailwind runserver` en lugar de `runserver`, o
  `tailwind build` una vez. La primera vez descarga el binario (unos 100 MB), así
  que requiere internet y puede tardar minutos. Está en el README.
- El CSS compilado no se sube al repositorio, para que los PR en paralelo no
  choquen en un archivo generado. El despliegue (ADR 0003) deberá correr
  `tailwind build` antes de `collectstatic`.
- Las pruebas y la CI no necesitan el CSS compilado.
- El binario se descarga de GitHub sin verificación de sumas de comprobación,
  según la documentación del paquete. Fijar la versión limita ese riesgo; al
  subirla, conviene comparar la suma con la del release.
- `DESIGN.md` está en `alpha` y su formato puede cambiar. En el peor caso queda
  como documentación de diseño. Quien cambie un valor de `DESIGN.md` o del bloque
  `@theme` cambia el otro en el mismo PR; la prueba lo recuerda.
