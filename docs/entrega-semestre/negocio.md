# EngiMods: modelo de negocio

Las cifras de este modelo son hipótesis o estimaciones históricas, no resultados. El contexto de producto se encuentra en [docs/negocio.md](../negocio.md).

## Problema, público y propuesta

Quienes quieren crear mods suelen encontrar recursos dispersos, dependientes de versiones y centrados en fragmentos de código, sin una ruta completa para probar, documentar, publicar y mantener su creación. Esta es una **hipótesis de problema**, no una demanda cuantificada. El público inicial propuesto son personas hispanohablantes, principalmente en México, con computadora, acceso al juego y programación básica; también podrían participar administradores de servidores interesados en aprender.

EngiMods propone una academia multi-juego en español: ejercicios prácticos, ingeniería de software aplicada y referencia explícita a la versión del juego y al entorno con que se probó cada lección. El valor buscado es ayudar a construir un mod propio y recibir retroalimentación, no solo copiar código. El juego inicial, la duración del acceso y los textos legales siguen por decidirse.

El material previo de descubrimiento registra una conversación disponible y cuatro casos simulados, no cinco entrevistas. No hay evidencia de ventas, alumnos reales ni validación comercial. El código integrado muestra avance de construcción, pero no demuestra por sí solo interés de mercado ni una experiencia completa ensayada.

## Oferta y alcance

| Oferta | Hipótesis de producto, no venta realizada |
|---|---|
| Misión Cero | Práctica corta **autoguiada**, sin grupo ni fecha de inicio compartida, para producir un cambio funcional. Precio propuesto: MXN 199 en piloto y, después, probar MXN 299. Acceso por tiempo; días pendientes. |
| Curso principal | Oferta futura de seis semanas, hasta ocho plazas por grupo, clínicas y revisión propuesta en 24 horas; MXN 1,990 por alumno. Los grupos/cohortes no están implementados como producto operativo. La revisión en 24 horas es una promesa por validar, no un resultado medido. |

El MVP busca probar el valor de una práctica con contenido y retroalimentación; el MVE plantea el recorrido descubrir → iniciar → recibir valor → confiar/cerrar → volver o recomendar. Hay componentes integrados para distintas etapas, pero el recorrido completo no se ha demostrado. Una muestra académica puede usar datos de prueba identificados, sin abrir un negocio real, cobrar ni incorporar alumnos reales.

En la observación pública del **16 de noviembre**, el registro estaba bloqueado por falta de aviso vigente, privacidad y términos respondían 404, y se mostraba un juego y un curso ficticios cuyo temario no estaba publicado. Esa observación es histórica: no se reverificó ni se probó el flujo autenticado para este documento. En el alcance académico se usa Stripe en modo prueba y el correo sale por consola; no equivalen a pagos ni a correo real.

## Canvas actualizado: modelo multi-juego

| Bloque | Modelo propuesto y cuestiones por validar |
|---|---|
| Segmentos de clientes | Aficionados hispanohablantes con programación básica y juego compatible, inicialmente México; validar interés por juego y necesidades. |
| Propuesta de valor | Ruta práctica en español para crear un mod propio, con ingeniería, información de versión probada y retroalimentación. Validar que resuelva el problema percibido. |
| Canales | Sitio web y, como difusión futura, videos, comunidades de Discord y recomendaciones; permisos y canales concretos por acordar. |
| Relación con clientes | Apoyo inicial y revisión de entregas; comunidad y seguimiento como propuestas. La atención en 24 horas pertenece a la oferta futura y requiere medición. |
| Fuentes de ingreso | Precio hipotético de Misión Cero y curso posterior, separados por producto; membresía y talleres aún por definir. Sin ingresos reales comprobados. |
| Recursos clave | Plataforma, contenido probado por versión y juego, personas con dominio técnico y pedagógico, infraestructura y medios de pago. |
| Actividades clave | Diseñar y probar ejercicios; mantener compatibilidad; revisar entregas; operar soporte, acceso y medición cuando se autorice un piloto. |
| Socios clave | Posibles creadores de mods y administradores de comunidades; proveedores de alojamiento, pagos y correo. No se afirman alianzas comerciales cerradas. |
| Estructura de costos | Plataforma, horas de tutoría y mantenimiento, comisiones, adquisición, contenido, impuestos y devoluciones. Cada juego adicional requiere contenido y revalidación propios. |

## Viabilidad: estimaciones históricas, no presupuesto vigente

El [lienzo resumido en la fuente de producto](../negocio.md#números-del-lienzo-estimaciones) documenta estimaciones del 28 de septiembre de 2026, anteriores al pivote multi-juego. Son un escenario para el **curso de seis semanas**, no para Misión Cero:

| Concepto histórico | Estimación y límite |
|---|---|
| Plataforma por grupo | MXN 900 estimados. |
| Tutoría y mantenimiento | 36 horas × MXN 300 = MXN 10,800 estimados. Costo fijo base total: MXN 11,700. |
| Ingreso de referencia | 8 plazas × MXN 1,990 = MXN 15,920 hipotéticos, no ventas. |
| Comisión base | MXN 597.12 estimados con 3.6 % + MXN 3 por pago, antes del IVA de la comisión; tarifa consultada el 28/09 y pendiente de verificar. |
| Saldo y equilibrio | MXN 3,622.88 después del costo fijo y comisión base; equilibrio estimado de 7 plazas bajo esos supuestos. No es utilidad neta. |

El escenario excluye impuestos, captación, contenido inicial y devoluciones; también omite el costo adicional de preparar y revalidar contenido para más juegos. El lienzo proponía para un piloto **hasta MXN 1,500 y 12 horas propias**: es una propuesta histórica, no gasto registrado ni presupuesto vigente aprobado. El uso de planes gratuitos de Render y Neon para staging no valida los costos de una operación comercial. Antes de decidir viabilidad hay que actualizar tarifas, alcance, costos y capacidad.

## Plan de trabajo al 18 de noviembre

Los responsables de las tareas restantes deben confirmarse con el equipo. Las fechas corresponden a 2026.

| Cuándo | Acción | Estado al corte | Responsable propuesto |
|---|---|---|---|
| 17 nov | Documentar arquitectura y requisitos, reunir evidencia de aportaciones y preparar la explicación técnica. | Documentación y evidencias preparadas; revisión del equipo pendiente. | Fabián. |
| 17–18 nov | Revisar el modelo y resolver decisiones de negocio. | Falta validación. | Pedro, sujeto a aceptación y apoyo del equipo. |
| 17–18 nov | Integrar la presentación y acordar la exposición. | Faltan revisión, materiales y reparto. | Pedro y equipo, propuesta por confirmar. |
| 17–18 nov | Acordar alcance de demo y evidencia; ensayar solo si el equipo lo autoriza y dispone de condiciones. | Pendiente; recorrido completo no comprobado aquí. | Equipo; operador por confirmar. |
| 18 nov | Revisar la coherencia entre negocio, presentación y documentación técnica. | Pendiente. | Equipo. |

## Marketing operativo: propuesta posterior a aprobación

El objetivo es saber si el público entiende el valor de una práctica de modding y muestra interés en Misión Cero, antes de considerar un lanzamiento comercial. No hay campaña ejecutada ni resultados que reportar.

La audiencia son personas con programación básica interesadas en modificar juegos compatibles. El mensaje a probar es: «Aprende a construir tu propio mod con una ruta en español y referencias claras de versiones». No se debe prometer un juego concreto, una fecha de acceso ni revisión en 24 horas para Misión Cero sin acuerdo y evidencia.

La oferta sería la práctica autoguiada; si se aprueba un piloto, se podría contrastar el interés a MXN 199 y probar MXN 299 después. Los canales propuestos son videos, comunidades que permitan la publicación y recomendaciones. La publicidad, el registro de datos personales y los cobros requieren aprobación previa.

No existe presupuesto actual confirmado. La propuesta histórica de hasta MXN 1,500 y 12 horas no autoriza gasto. Para el 17–18 de noviembre se propone revisar mensaje y métricas. La muestra gratuita y la lista de espera son propuestas, no componentes disponibles.

Para un piloto posterior se propone la siguiente secuencia de una semana, como hipótesis de trabajo y no como compromiso. El día 0 comienza únicamente cuando el equipo lo apruebe; Pedro y el equipo deben confirmar la duración y asignar a una persona responsable. La difusión y la participación requieren además que el recorrido y la operación estén listos, que las condiciones legales estén resueltas y que exista consentimiento para el registro de datos. La secuencia comienza cuando se cumplan esas condiciones.

| Momento | Actividad propuesta |
|---|---|
| Día 0 | Acordar oferta, juego, acceso, condiciones legales, forma de medición, ventana de observación y responsable; comprobar que el recorrido y la operación estén listos. |
| Días 1–2 | Preparar y revisar el mensaje y una pieza de difusión acordes con la oferta. |
| Días 3–5 | Solo con aprobación, difundir en comunidades que lo autoricen; registrar consultas e inicios con consentimiento y sin recopilar datos innecesarios. |
| Días 6–7 | Observar la finalización dentro de la ventana acordada, revisar los registros disponibles y decidir si continuar, ajustar o pausar. Si la ventana requiere más tiempo, acordarlo antes de sacar conclusiones. |

La secuencia no autoriza gastos ni convierte los días propuestos en fechas de lanzamiento.

| Indicador propuesto | Cálculo y fuente futura | Regla de decisión propuesta, sujeta a aprobación |
|---|---|---|
| Comprensión de la oferta | Personas que explican correctamente el beneficio / personas consultadas; registro voluntario de conversaciones reales. | Acordar antes el tamaño y umbral; si no se alcanza, aclarar mensaje y repetir. Sin respuestas no se calcula. |
| Interés por juego | Personas que expresan interés por juego / personas consultadas; registro con consentimiento y sin confundir casos simulados con respuestas. | Comparar interés y capacidad de producir contenido probado; si no hay señal suficiente, investigar antes de elegir. |
| Conversión al inicio | Inicios de Misión Cero / visitas elegibles a la oferta; eventos o conteo manual definido antes del piloto. | Acordar umbral y ventana antes de medir; si no se alcanza, revisar requisitos y recorrido. Sin visitas, indicador no calculable. |
| Finalización | Personas que terminan / personas que iniciaron; registro de avance del piloto. | Acordar umbral; si no se alcanza, revisar dificultades de contenido y soporte. Sin inicios, no se calcula. |
| Revisión en 24 horas | Revisiones dentro de 24 h / entregas revisadas del curso futuro; fechas de envío y respuesta. | Acordar objetivo y medición antes de prometer el servicio; si no se sostiene, ajustar capacidad o promesa. Sin revisiones, no se calcula. |

La instrumentación y el tablero de métricas son trabajo futuro; no se afirma que estos eventos estén disponibles o se hayan medido. Para decidir continuar, ajustar o pausar se necesitarán umbrales aprobados, muestra, ventana y evidencia real; no se sustituye esa decisión con casos simulados.

## Aspectos por confirmar

| Decisión o dato faltante | Qué revisar o resolver | Estado |
|---|---|---|
| Oferta y legal | Elegir juego inicial y días de acceso; acordar responsable y textos legales aplicables. | Sin decisión registrada aquí; no inventar. |
| Demo | Definir qué recorrido se puede mostrar, quién lo prepara y qué evidencia existe; si no se ensaya, exponer límites. | Pendiente; observación pública histórica del 16. |
| Marketing y viabilidad | Aprobar o corregir mensaje, canal, presupuesto, ventana, muestra, umbrales y costos actualizados. | Solo hipótesis y cifras históricas. |
| Presentación | Completar aportaciones del resto del equipo, elegir capturas verificables y acordar quién explica cada sección. | Pendiente. |

## Fuentes de producto

- [Contexto de negocio e hipótesis](../negocio.md).
- [Arquitectura y reglas](../arquitectura.md) y [backlog de producto](../BACKLOG.md).
- [Estado de referencia del repositorio, 14 de noviembre](https://github.com/Alexis01000011/EngiMods/tree/539f1e0a866571d11ee7b53f9e14d946f4f33a74).
