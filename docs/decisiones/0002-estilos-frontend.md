# 0002. Estilos del frontend

- Estado: Propuesta
- Fecha: 2026-11-03
- Historia: EM-004

## Contexto

La entrega de semestre requiere páginas de Django, navegación y mensajes que se
puedan usar a 360 px. Son tres personas, el presupuesto total del piloto es
MXN 1,500 y queda alrededor de un mes. El ADR 0001 mantiene plantillas del
servidor. No hay un enfoque de estilos elegido ni una cadena de compilación CSS.

## Opciones consideradas

Fuentes consultadas el 2026-11-03. Los costos siguientes son de herramientas;
el trabajo de implementación y mantenimiento no está monetizado.

| Opción | Costo mensual de herramienta | Configuración y compatibilidad | Ventajas y límites |
|---|---|---|---|
| CSS propio pequeño | MXN 0 / USD 0 | Un archivo en `static/`, incluido por `base.html`; sin efecto en PostgreSQL | Pocas piezas y sin compilación. El equipo debe diseñar y mantener formularios, estados, foco y navegación adaptable. |
| Bootstrap | MXN 0 / USD 0 por el paquete MIT | CSS distribuido por el proyecto; JavaScript solo para componentes que lo necesiten. Compatible con plantillas Django | Componentes y rejilla disponibles; hay que adaptar la apariencia y comprobar accesibilidad. Conservar avisos de licencia. |
| Tailwind CSS | MXN 0 / USD 0 por el paquete MIT | Compilar a un archivo estático con CLI; existe CLI independiente, además de la opción con npm. Compatible con plantillas Django | Facilita componer estilos con utilidades. Añade un paso reproducible de compilación y detección de clases en plantillas. |

Fuentes: [inicio de Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/),
[licencia de Bootstrap](https://getbootstrap.com/docs/5.3/about/license/),
[Tailwind CLI](https://tailwindcss.com/docs/installation/tailwind-cli) y
[licencia de Tailwind](https://github.com/tailwindlabs/tailwindcss/blob/main/LICENSE).
No se incluyen plantillas, temas ni componentes comerciales.

Las tres alternativas permiten implementar EM-004 y dar una base a las páginas
posteriores. Ninguna afecta los modelos ni exige frontend separado. Cambiar CSS
propio por una biblioteca requeriría adaptar clases; cambiar Bootstrap por
Tailwind exigiría revisar más marcado. Esto es una valoración de mantenimiento,
no una medición de horas del equipo.

## Decisión

**Recomendación: CSS propio pequeño para el recorte**, con variables para colores
y espaciado, componentes compartidos de formulario y reglas adaptables. Reduce la
configuración necesaria para las pocas pantallas iniciales. Si el equipo ya domina
Bootstrap o Tailwind, ese conocimiento puede justificar otra opción.

**Falta la decisión del equipo.** Este ADR no autoriza implementar un enfoque ni
marca EM-004 como hecha. No sustituye la revisión visual de cada pantalla.

## Consecuencias

Si se acepta, EM-004 implementará navegación, pie, mensajes y estilos; verificará
360 px y escritorio, teclado, contraste y estados de error. Se evitarán estilos
duplicados en cada plantilla. El equipo será responsable de mantener esa base.

Si se elige una biblioteca, antes de agregarla se documentarán versión, licencia,
forma de distribución y compilación si aplica. La incorporación se hará en EM-004.
