# 0002. Estilos del frontend

- Estado: Propuesta
- Fecha: 2026-11-03 (actualizada el 2026-11-04)
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

**Recomendación (propuesta por Alexis el 2026-11-04): Tailwind CSS v4 con
`django-tailwind-cli` y un `DESIGN.md` en la raíz del repositorio.**

- `DESIGN.md` describe la identidad visual como la documentación oficial de un
  kit de desarrollo de mods: fondo claro, un solo acento índigo, fuentes del
  sistema y el sello "Probado con" siempre visible. Pasa el linter oficial
  (`@google/design.md` 0.4.0) sin errores ni advertencias.
- Tailwind convierte esos valores en clases que se usan directamente en las
  plantillas. Así, cada pantalla aplica el mismo sistema sin que alguien tenga
  que mantener a mano una hoja de estilos compartida.
- `django-tailwind-cli` evita Node, funciona en Windows y en Arch, y deja la
  compilación dentro de `manage.py`.

Esta recomendación reemplaza la anterior, que era CSS propio pequeño. CSS propio
sigue siendo la opción con menos piezas, y `DESIGN.md` serviría igual con él.
Lo que cambia la balanza es que hay varias personas y agentes creando pantallas
en paralelo: con utilidades, el sistema queda en las clases y no en reglas CSS
que se pueden duplicar o contradecir.

**Falta la decisión del equipo.** Este ADR no autoriza implementar un enfoque ni
marca EM-004 como hecha. No sustituye la revisión visual de cada pantalla.

## Consecuencias

Si se acepta, EM-004:

- Agregará `django-tailwind-cli` con `uv add`, con `TAILWIND_CLI_VERSION` fijada
  en una versión concreta y no en `latest`.
- Pondrá el CSS fuente fuera de `static/` y su bloque `@theme` con los valores de
  `DESIGN.md`, e ignorará en git la carpeta del binario descargado
  (`.django_tailwind_cli/`).
- Implementará navegación, pie, mensajes y estilos siguiendo `DESIGN.md`, y
  verificará 360 px y escritorio, teclado, contraste y estados de error.
- Agregará a `AGENTS.md` que las pantallas siguen `DESIGN.md`, para que Claude y
  Codex lo lean antes de tocar plantillas.

También cambia el trabajo diario:

- Para ver los estilos en desarrollo hay que correr
  `uv run python manage.py tailwind runserver` en lugar de `runserver`, o
  `tailwind build` una vez. La primera vez descarga el binario, así que
  requiere internet. Hay que documentarlo en el README.
- El CSS compilado no se sube al repositorio, para que los PR en paralelo no
  choquen en un archivo generado. El despliegue (ADR 0003) deberá correr
  `tailwind build` antes de `collectstatic`.
- Las pruebas y la CI no necesitan el CSS compilado.
- El binario se descarga de GitHub sin verificación de sumas de comprobación,
  según la documentación del paquete. Fijar la versión limita ese riesgo.
- `DESIGN.md` está en `alpha` y su formato puede cambiar. En el peor caso queda
  como documentación de diseño. Mantener el bloque `@theme` igual que
  `DESIGN.md` es responsabilidad de quien cambie cualquiera de los dos; el CLI
  de Google puede regenerarlo.

Si el equipo prefiere CSS propio, `DESIGN.md` se conserva y sus valores pasan a
variables CSS en un archivo de `static/`, sin compilación.
