# EngiMods: modelo de negocio y plan de marketing

Equipo 8 · Negocios Electrónicos · Ingeniería de Software · UAZ · Semestre agosto–diciembre 2026.

El contexto completo de producto está en [docs/negocio.md](../negocio.md). Las cifras marcadas como estimación provienen del lienzo del 28/09/2026 y se presentan como escenarios de planeación, no como resultados.

## 1. Problema

Los recursos para crear mods de videojuegos están dispersos, dependen de versiones específicas y se centran en fragmentos de código. No existe una ruta completa en español que lleve al alumno desde la idea hasta un mod publicado, con prácticas de ingeniería de software: arquitectura, Git, pruebas, documentación y mantenimiento.

**Evidencia recopilada:** una conversación con un creador de mods activo y cuatro casos simulados que exploran los escenarios de uso. No se realizaron entrevistas formales a cinco personas; la validación de demanda real queda como objetivo del piloto.

## 2. Público objetivo

| Característica | Detalle |
|---|---|
| Perfil | Jugadores y aficionados hispanohablantes que quieren personalizar sus juegos, principalmente en México |
| Requisitos | Computadora, acceso al juego, programación básica (variables, funciones, condicionales) |
| También incluye | Administradores de servidores que quieren aprender a crear mods, no solo instalarlos |
| No requiere | Ser desarrollador profesional ni tener experiencia en ingeniería de software |

## 3. Propuesta de valor

**Aprende a construir tu propio mod con una ruta práctica en español, con ingeniería de software aplicada y referencias claras de versiones.**

Diferenciadores:

1. **Multi-juego por diseño.** La plataforma no está atada a un juego: los juegos, versiones y entornos de modding son datos del catálogo. El piloto arranca con Minecraft: Java Edition y Hytale.
2. **Versión probada.** Cada lección indica con qué versión del juego y del entorno fue probada. Cuando sale una versión nueva, el contenido se marca como pendiente de revalidar.
3. **Retroalimentación real.** El alumno construye un mod propio y un tutor lo revisa con rúbrica, no solo ve videos y copia código.
4. **Ingeniería desde el inicio.** Git, pruebas, documentación y publicación desde la primera lección.

## 4. Oferta de productos

| Producto | Formato | Precio | Estado |
|---|---|---|---|
| **Misión Cero** | Práctica corta autoguiada, sin grupo ni fecha de inicio compartida. El alumno produce un cambio funcional en el juego. | MXN 199 (piloto); después probar MXN 299 | Plataforma implementada. Contenido borrador para Minecraft (Fabric). |
| **Curso principal** | Seis semanas, hasta 8 plazas por grupo, clínicas grupales semanales, revisión de entregas en 24 h | MXN 1,990 por alumno | Diseño del temario. Los grupos (cohortes) no están implementados. |
| **Membresía** (futuro) | Acceso a actualizaciones de contenido cuando salen versiones nuevas | Por definir | Concepto. |

**Acceso por tiempo:** el contenido de Misión Cero se desbloquea al pagar y permanece disponible por un número limitado de días. Para Minecraft se decidieron 30 días; Hytale y el curso quedan por definir.

## 5. Canvas del modelo de negocio

| Bloque | Contenido |
|---|---|
| **Segmentos de clientes** | Jugadores hispanohablantes con programación básica que quieren crear mods. Inicio: México. Segmento secundario: administradores de servidores. |
| **Propuesta de valor** | Ruta práctica en español para construir un mod propio, con ingeniería de software, versiones probadas y retroalimentación de un tutor. |
| **Canales** | *Difusión:* videos en YouTube, comunidades de Discord de modding, recomendaciones boca a boca. *Venta:* sitio web con landing, temario, lección de muestra y pago en línea. *Entrega:* lecciones web, repositorios plantilla en GitHub, comunidad en Discord. |
| **Relación con clientes** | Revisión de entregas con rúbrica. Comunidad en Discord para preguntas. Avisos cuando el contenido se actualiza por nueva versión. Para el curso futuro: clínicas grupales semanales y revisión en 24 h. |
| **Fuentes de ingreso** | Misión Cero (MXN 199–299 por persona). Curso principal (MXN 1,990 por alumno, hasta 8 por grupo). Membresía de actualizaciones (futuro). Talleres personalizados bajo cotización (futuro). |
| **Recursos clave** | Plataforma web (Django, Render, Neon). Contenido probado por versión y por juego. Personas con dominio técnico y pedagógico en modding. Infraestructura de pagos (Stripe). |
| **Actividades clave** | Diseñar y probar ejercicios para cada juego. Mantener compatibilidad con versiones nuevas. Revisar entregas de alumnos. Operar el soporte, el acceso y la medición del piloto. Producir material de difusión. |
| **Socios clave** | Creadores de mods con experiencia (revisión de ejercicios, difusión a cambio de talleres y reconocimiento). Administradores de comunidades de Discord. Proveedores: Render (hosting), Neon (base de datos), Stripe (pagos), proveedor de correo transaccional (por elegir). |
| **Estructura de costos** | *Fijos:* plataforma, horas de tutoría, producción de contenido. *Variables:* comisión de Stripe (3.6 % + MXN 3 por pago), mantenimiento de contenido por versión. *Por juego adicional:* contenido y revalidación propios. Ver sección 6 para el desglose. |

## 6. Viabilidad económica

### Escenario: curso de seis semanas (8 plazas)

Estimaciones del lienzo del 28/09/2026 para un solo juego. El escenario es un punto de partida para planeación, no un presupuesto aprobado.

| Concepto | Monto estimado |
|---|---|
| Plataforma (hosting, base de datos) | MXN 900 por grupo |
| Tutoría y mantenimiento (36 h × MXN 300/h) | MXN 10,800 por grupo |
| **Costo fijo base** | **MXN 11,700** |
| Ingreso bruto (8 × MXN 1,990) | MXN 15,920 |
| Comisión Stripe estimada (3.6 % + MXN 3 × 8) | MXN 597 |
| **Margen antes de impuestos** | **MXN 3,623** |
| **Punto de equilibrio** | **7 plazas** |

**No incluye:** impuestos (ISR, IVA), costos de captación de alumnos, producción del contenido inicial, devoluciones ni el costo de agregar juegos adicionales. La tarifa de Stripe fue consultada el 28/09/2026 y requiere verificación.

### Escenario: Misión Cero

| Concepto | Valor |
|---|---|
| Precio piloto | MXN 199 por persona |
| Costo variable (Stripe) | ~MXN 10 por pago |
| Costo fijo de plataforma | Absorbido por planes gratuitos durante el piloto (Render, Neon) |
| Costo de contenido | Producción inicial, luego mantenimiento por versión |

Misión Cero es el producto de entrada y validación. Su margen por unidad es bajo, pero su propósito principal es validar la propuesta de valor y convertir alumnos al curso de seis semanas.

### Inversión inicial para piloto

Propuesta del lienzo: hasta **MXN 1,500 de gasto** y **12 horas propias** para probar la oferta. Durante el semestre se utilizaron planes gratuitos (Render, Neon, Stripe en modo prueba), sin desembolso real.

## 7. Recorrido del cliente (MVE)

| Etapa | Qué vive el cliente | Implementado |
|---|---|---|
| **Descubrir** | Llega al sitio, ve la landing, explora el catálogo de juegos y el detalle del curso con precio, requisitos y temario | Landing, catálogo, detalle del curso |
| **Iniciar** | Se registra con correo, acepta el aviso de privacidad, verifica su cuenta, inicia sesión y paga con Stripe | Registro, consentimiento, verificación, sesión, Checkout |
| **Recibir valor** | Queda inscrito, ve su panel con el avance, entra a las lecciones con la etiqueta "Probado con" y sigue los pasos | Inscripción, panel del alumno, lecciones, avance |
| **Confiar/cerrar** | Entrega su ejercicio (enlace a su repositorio), recibe la revisión del tutor con rúbrica y comentarios, puede reenviar si se piden cambios | Entregas, cola de revisión, rúbrica, reenvío |
| **Volver** | Termina el curso, ve su progreso, recomienda a otros | Panel de avance, métricas del piloto (admin) |

**MVP (Mecanismo de Valor del Producto):** el alumno completa una práctica que produce un cambio funcional en el juego y recibe retroalimentación estructurada.

**MVE (Mínima Experiencia Viable):** el recorrido completo desde descubrir la oferta hasta terminar y potencialmente recomendar.

**Estado al 17 de noviembre de 2026:** las siete apps que cubren el recorrido están implementadas y desplegadas en staging con Stripe en modo prueba. El correo sale por consola (el envío real quedó fuera del recorte de semestre). El contenido de Misión Cero para Minecraft tiene borradores sin probar en el juego.

## 8. Plan de marketing

### 8.1. Objetivo

Validar si el público entiende la propuesta y muestra interés en Misión Cero antes de considerar un lanzamiento comercial.

### 8.2. Mensaje central

> «Aprende a construir tu propio mod con una ruta en español y referencias claras de versiones.»

El mensaje se prueba en conversaciones y en las piezas de difusión. Se ajusta según la comprensión observada.

### 8.3. Audiencia y canales

| Canal | Acción | Costo estimado |
|---|---|---|
| **Comunidades de Discord** de Minecraft y Hytale en español | Publicar en canales que permitan autopromociones, con un mensaje corto y enlace al sitio | Gratuito (tiempo propio) |
| **YouTube** | Video corto (2–3 min) mostrando qué hace el alumno en Misión Cero y qué logra al terminar | Producción propia; sin pauta |
| **Reddit** (r/feedthebeast, r/fabricmc, r/Hytale) | Post en español e inglés explicando la propuesta para comunidades relevantes | Gratuito |
| **Recomendaciones** | Pedir a alumnos del piloto que compartan su experiencia si les fue útil | Gratuito |
| **Redes sociales** | Cuenta de EngiMods para publicar avances y tips de modding | Gratuito |

**Presupuesto de marketing:** MXN 0 en la fase de validación. El presupuesto del lienzo (MXN 1,500) se reserva para pauta en caso de que la difusión orgánica no genere tráfico suficiente.

### 8.4. Embudo de conversión

```
Visitantes al sitio
  → Ven la landing y el catálogo
    → Se registran y verifican correo
      → Ven el detalle del curso y el precio
        → Pagan Misión Cero (MXN 199)
          → Completan las lecciones
            → Entregan el ejercicio
              → Reciben la revisión del tutor
```

### 8.5. Secuencia del piloto (una semana)

La secuencia comienza cuando el equipo lo apruebe y el recorrido esté listo en staging.

| Día | Actividad |
|---|---|
| 0 | Acordar oferta, juego, condiciones legales, ventana de observación y responsable. Verificar que staging está operativo. |
| 1–2 | Preparar y revisar el mensaje y una pieza de difusión (video o publicación). |
| 3–5 | Difundir en comunidades que lo autoricen. Registrar consultas e inicios con consentimiento. |
| 6–7 | Observar la finalización, revisar los registros disponibles y decidir si continuar, ajustar o pausar. |

### 8.6. Métricas del piloto

| Indicador | Cómo se mide | Decisión |
|---|---|---|
| **Comprensión** | Personas que explican el beneficio correctamente / personas consultadas | Si es baja, aclarar el mensaje y repetir |
| **Interés por juego** | Personas que expresan interés / personas consultadas, separado por juego | Comparar interés con capacidad de producir contenido |
| **Conversión al inicio** | Inscripciones a Misión Cero / visitas a la página del curso | Si es baja, revisar precio, requisitos o recorrido |
| **Finalización** | Alumnos que terminan / alumnos que iniciaron | Si es baja, revisar dificultad y soporte |
| **Tiempo de revisión** | Revisiones dentro de 24 h / entregas revisadas | Si no se sostiene, ajustar capacidad o promesa |

La plataforma ya tiene un tablero de métricas del piloto para administradores (EM-091), con inscripciones, avance, entregas e ingresos.

### 8.7. Estrategia de precios

| Fase | Misión Cero | Curso |
|---|---|---|
| Piloto | MXN 199 | No disponible (grupos no implementados) |
| Post-validación | Probar MXN 299 y comparar conversión | MXN 1,990 |
| Si la conversión baja | Ofrecer cupón de primer intento o extender días de acceso | Ajustar precio o cupo |

## 9. Plataforma construida

La plataforma se construyó durante el semestre con 31 historias de usuario completadas, 539 pruebas automatizadas y 7 aplicaciones Django:

| App | Función |
|---|---|
| `core` | Landing, páginas legales, utilidades compartidas |
| `accounts` | Registro, verificación, sesión, rol de tutor, consentimiento |
| `catalog` | Catálogo multi-juego, versiones, entornos de modding |
| `courses` | Cursos, módulos, lecciones con "Probado con", ejercicios, rúbricas |
| `enrollments` | Inscripciones por tiempo, panel del alumno, avance |
| `payments` | Checkout de Stripe y webhook de confirmación |
| `submissions` | Entregas, cola de revisión, revisión con rúbrica, reenvío |

**Infraestructura:** Render (web) y Neon (PostgreSQL), ambos en planes gratuitos para el piloto. Stripe en modo prueba. CI con GitHub Actions (lint, formato, migraciones y pruebas en cada PR).

## 10. Decisiones pendientes

| Decisión | Qué implica |
|---|---|
| Días de acceso de Hytale y del curso | Dato configurable por curso; los decide el equipo |
| Textos legales (aviso de privacidad, términos, política de devolución) | Bloquean el registro público; el equipo debe redactarlos y definir al responsable legal |
| Proveedor de correo transaccional | El correo sale por consola; para un piloto real se necesita un servicio HTTPS con dominio propio |
| Contenido de Hytale | El borrador de Minecraft existe; Hytale requiere verificación de herramientas (acceso anticipado) |
| Presupuesto de pauta | MXN 1,500 del lienzo es una propuesta; requiere aprobación |

## Fuentes

- [Contexto de negocio e hipótesis](../negocio.md)
- [Arquitectura y reglas](../arquitectura.md)
- [Backlog de producto](../BACKLOG.md)
- [Plan de contenido: Hytale y Minecraft](../contenido/plan-hytale-minecraft.md)
- [Repositorio (commit de referencia)](https://github.com/Alexis01000011/EngiMods/tree/51e539c)
