# EngiMods: presentación

---

## Diapositiva 1 — EngiMods: aprender ingeniería creando mods

- Academia propuesta en español y multi-juego.
- Equipo 8 · Negocios Electrónicos.
- MVP, MVE y modelo de negocio.

**Notas:** Presentar el proyecto y aclarar que la oferta comercial es una propuesta.

---

## Diapositiva 2 — Problema y evidencia disponible

- Recursos dispersos y dependientes de versiones: hipótesis de problema.
- Público inicial: hispanohablantes con juego, computadora y programación básica.
- Una conversación disponible y cuatro casos simulados.
- Sin evidencia aquí de cinco entrevistas, ventas ni validación comercial.

**Notas:** Los casos simulados ayudan a explorar escenarios, pero no cuentan como entrevistas. Falta contrastar el problema con más personas.

---

## Diapositiva 3 — Propuesta de valor y Canvas

- Ruta práctica: mod propio, Git, pruebas y documentación.
- Lecciones con versión del juego y entorno probado.
- Canales propuestos: web, videos y comunidades.
- Recursos y costos: contenido por juego, tutoría e infraestructura.
- Ingresos hipotéticos; aliados y demanda por validar.

**Notas:** El Canvas anterior estaba centrado en Hytale; el actual contempla varios juegos. Consultar los [nueve bloques](negocio.md#canvas-actualizado-modelo-multi-juego).

---

## Diapositiva 4 — Oferta y viabilidad

- Misión Cero: práctica autoguiada; MXN 199 en piloto y prueba posterior de MXN 299.
- Curso futuro: seis semanas, hasta ocho plazas, MXN 1,990 por alumno.
- Atención en 24 horas: propuesta del curso, no servicio medido.
- Cifras y costos históricos son estimaciones, no cobros.

**Notas:** Los precios corresponden a productos distintos. Los grupos del curso futuro no están implementados; faltan el juego inicial y los días de acceso. El escenario histórico omite captación y contenido adicional por juego.

---

## Diapositiva 5 — MVP y MVE: recorrido y brechas

- MVP propuesto: práctica con cambio funcional y retroalimentación.
- MVE: descubrir → iniciar → recibir valor → confiar/cerrar → volver.
- Hay componentes integrados; el recorrido completo no se ha verificado aquí.
- Stripe de prueba y correo por consola; sin alumnos ni dinero reales.

**Notas:** El 16 de noviembre, sin autenticación, se observó registro bloqueado, páginas legales con 404 y un curso ficticio sin temario publicado. No se reverificó. Explicar qué se muestra realmente y qué falta: código integrado no equivale a una demo completa.

---

## Diapositiva 6 — Arquitectura y operación

- Monolito Django 5.2 y Python; plantillas de servidor y Tailwind.
- Render y Neon para staging; Stripe en modo prueba.
- Catálogo, cuentas, cursos, inscripción, pagos y entregas.
- Grupos y tablero de métricas: previstos, no implementados.

**Notas:** Explicar el flujo de visitante a revisión sin afirmar que se ensayó completo. El webhook confirma el pago de prueba; el correo real está fuera del recorte. Referencia: [arquitectura](../arquitectura.md).

---

## Diapositiva 7 — Aportaciones técnicas de Fabián

- [EM-010: catálogo de juegos, PR 75](https://github.com/Alexis01000011/EngiMods/pull/75).
- [EM-011: versiones y entornos, PR 79](https://github.com/Alexis01000011/EngiMods/pull/79).
- [EM-035: rol de tutor, PR 76](https://github.com/Alexis01000011/EngiMods/pull/76).
- Catálogo multi-juego y permisos diferenciados.

**Guion — Fabián:** «En EM-010 trabajé el catálogo para representar cada juego como dato, sin limitar la plataforma a uno solo. En EM-011 añadí versiones, entornos y compatibilidades. Esto permite indicar con qué combinación se probó el contenido. En EM-035 trabajé el rol de tutor: no es lo mismo ser tutor que administrador, y las pantallas de tutoría comprueban permisos. Estas piezas apoyan el modelo multi-juego, aunque por sí solas no prueban toda la demo».

**Notas de defensa:** Mostrar los PR como respaldo de las historias, no como prueba de usuarios o ventas. La revalidación automática al salir una versión nueva es trabajo pendiente, según el [backlog](../BACKLOG.md).

---

## Diapositiva 8 — Marketing y medición propuestos

- Audiencia: personas interesadas en modding con programación básica.
- Mensaje: construir un mod propio con una ruta en español.
- Canales posibles: videos, comunidades y recomendaciones.
- Medir comprensión, interés, inicio y finalización en un piloto autorizado.
- Presupuesto y umbrales actuales: por aprobar.

**Notas:** No se ha lanzado campaña. Los MXN 1,500 y 12 horas del lienzo son una propuesta anterior, no gasto ni presupuesto vigente. Para un piloto posterior se propone una semana: aprobar condiciones, preparar la pieza, difundir con permiso, observar y decidir. El inicio depende de aprobación, operación lista y consentimiento; Pedro y el equipo confirmarían la duración. Ver [marketing y calendario](negocio.md#marketing-operativo-propuesta-posterior-a-aprobación).

---

## Diapositiva 9 — Próximos pasos

- 17–18 de noviembre: revisar negocio, presentación y evidencia técnica.
- Confirmar responsables y alcance de la demo.
- Pendientes: juego inicial, acceso, textos legales y validación de mercado.
- Revisar el modelo con la evidencia disponible.

**Notas — reparto por confirmar:** Se propone que Pedro integre negocio y presentación con el equipo, y que Fabián explique sus aportaciones. Falta acordar quién prepara y ensaya la demo.

---

## Material visual por preparar

Solicitar al equipo capturas actuales solo si existen y pueden obtenerse de forma autorizada, sin datos personales ni secretos. No presentar esta lista como evidencia de pruebas realizadas:

| Captura necesaria | Qué debe demostrar y condición |
|---|---|
| Catálogo y detalle de juego | Que el catálogo muestra un juego de ejemplo identificado; registrar fecha y evitar afirmar soporte de juegos no cargados. |
| Versión, entorno y «probado con» | Una asociación real y visible de ejemplo, si el equipo la preparó; no atribuir una prueba de contenido que no se haya hecho. |
| Pantalla o evidencia de permisos de tutor | Diferencia entre acceso autorizado y denegado, únicamente si se ensaya y documenta. |
| Recorrido de demostración | Pantallas de cada etapa efectivamente ensayada con datos de prueba; identificar interrupciones y no inferir el resto del flujo. |
| Modelo o esquema de arquitectura | Relación entre componentes implementados y futuros; no presentarlo como captura de ejecución. |

**Revisión con el equipo:** completar las notas sin asignar autorías por inferencia, confirmar datos y capturas y atender los [aspectos por confirmar](negocio.md#aspectos-por-confirmar).
