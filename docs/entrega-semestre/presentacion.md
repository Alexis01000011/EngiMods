# EngiMods: presentación

---

## Diapositiva 1 — EngiMods: aprender ingeniería creando mods

- Academia en línea, en español, multi-juego.
- Mods de videojuegos con ingeniería de software.
- Equipo 8 · Negocios Electrónicos · UAZ.

**Notas:** Presentar al equipo y el concepto central: no es un curso para copiar código, es una ruta para construir un mod propio con prácticas de ingeniería.

---

## Diapositiva 2 — Problema y público

- Los recursos para crear mods están dispersos, dependen de versiones y no cubren el proceso completo.
- Público: jugadores hispanohablantes con programación básica, principalmente en México.
- Evidencia: una conversación con un creador activo y cuatro escenarios simulados.
- El piloto existe para validar la demanda real.

**Notas:** El problema se observó en foros y comunidades. Los cuatro casos simulados exploran los escenarios, pero la demanda real la mide el piloto. No se afirman cinco entrevistas formales.

---

## Diapositiva 3 — Propuesta de valor

- Ruta práctica en español: de la idea al mod publicado.
- Cada lección dice con qué versión del juego y del entorno fue probada.
- El alumno construye su mod; un tutor lo revisa con rúbrica.
- Ingeniería desde el inicio: Git, pruebas, documentación.

**Notas:** El diferenciador es la combinación de contenido por versión y retroalimentación real, no solo videos para seguir.

---

## Diapositiva 4 — Canvas del modelo de negocio

| Bloque | Resumen |
|---|---|
| Segmentos | Jugadores hispanohablantes con programación básica |
| Propuesta | Ruta práctica, versiones probadas, retroalimentación |
| Canales | Web, YouTube, Discord, recomendaciones |
| Relación | Revisión de entregas, comunidad, avisos de versión |
| Ingresos | Misión Cero (MXN 199), curso (MXN 1,990) |
| Recursos | Plataforma, contenido, tutores, infraestructura |
| Actividades | Producir contenido, revisar entregas, mantener versiones |
| Socios | Creadores de mods, comunidades, proveedores |
| Costos | Plataforma, tutoría, contenido, comisiones de Stripe |

**Notas:** Referencia completa en [negocio.md, sección 5](negocio.md#5-canvas-del-modelo-de-negocio). Cada juego adicional agrega su propio costo de contenido.

---

## Diapositiva 5 — Oferta y viabilidad

- **Misión Cero:** práctica autoguiada, MXN 199 en piloto, 30 días de acceso (Minecraft).
- **Curso futuro:** seis semanas, 8 plazas, MXN 1,990 por alumno.
- Punto de equilibrio del curso: 7 plazas con los supuestos del lienzo.
- Inversión del piloto: hasta MXN 1,500 y 12 horas propias.
- El semestre usó planes gratuitos (Render, Neon, Stripe de prueba): sin desembolso real.

**Notas:** Las cifras son estimaciones de planeación, no resultados. El escenario excluye impuestos y captación. Los precios son configurables en la plataforma.

---

## Diapositiva 6 — Recorrido del cliente y lo que construimos

```
Descubrir → Iniciar → Recibir valor → Confiar → Volver
```

| Etapa | Implementado |
|---|---|
| Descubrir | Landing, catálogo de juegos, detalle del curso |
| Iniciar | Registro, privacidad, verificación, sesión, Checkout |
| Recibir valor | Inscripción, panel del alumno, lecciones, avance |
| Confiar | Entregas, revisión con rúbrica, reenvío |
| Volver | Panel de avance, métricas del piloto |

- 31 historias completadas, 539 pruebas, 7 apps Django.
- Desplegado en staging (Render + Neon + Stripe de prueba).

**Notas:** El recorrido está implementado de punta a punta en código. El correo sale por consola (quedó fuera del recorte). El contenido de Misión Cero tiene borradores de Minecraft sin probar en el juego.

---

## Diapositiva 7 — Arquitectura

```
Navegador → Render (gunicorn) → Django 5.2
                                   ├── 7 apps
                                   ├── PostgreSQL (Neon)
                                   ├── Stripe Checkout
                                   └── Tailwind CSS
```

- Monolito Django con plantillas en el servidor. Sin frontend separado.
- CI en GitHub Actions: lint, formato, migraciones y pruebas en cada PR.
- Hosting gratuito: Render (web) y Neon (PostgreSQL), ambos en Ohio.
- El webhook de Stripe confirma el pago y crea la inscripción automáticamente.

**Notas:** Referencia completa en [arquitectura.md](../arquitectura.md). Los grupos y el tablero de métricas están previstos pero no implementados como apps separadas.

---

## Diapositiva 8 — Aportaciones de Pedro

- [EM-003: Modelo de usuario personalizado, PR #70](https://github.com/Alexis01000011/EngiMods/pull/70).
- [EM-009: Cuenta de Stripe en modo prueba, PR #71](https://github.com/Alexis01000011/EngiMods/pull/71).
- Coordinación del proyecto: backlog, issues, revisiones y decisiones de producto.

**Guion — Pedro:** «En EM-003 implementé el modelo de usuario personalizado con correo como identificador principal, en lugar del username de Django. Eso permite que el registro y la verificación funcionen por correo electrónico, que es lo que el alumno ya tiene. En EM-009 conecté la cuenta de Stripe en modo prueba: configuré las llaves, el endpoint del webhook y las variables de entorno para que el equipo pudiera construir el Checkout y el webhook encima. Además coordiné el backlog, asigné historias, revisé PRs y participé en las decisiones de producto como el pivote multi-juego y la elección de Minecraft y Hytale.»

**Evidencia:** [Issue #3](https://github.com/Alexis01000011/EngiMods/issues/3), [PR #70](https://github.com/Alexis01000011/EngiMods/pull/70), [Issue #9](https://github.com/Alexis01000011/EngiMods/issues/9), [PR #71](https://github.com/Alexis01000011/EngiMods/pull/71), [PR #72](https://github.com/Alexis01000011/EngiMods/pull/72).

---

## Diapositiva 9 — Aportaciones de Fabián

- [EM-010: Catálogo de juegos, PR #75](https://github.com/Alexis01000011/EngiMods/pull/75).
- [EM-011: Versiones y entornos, PR #79](https://github.com/Alexis01000011/EngiMods/pull/79).
- [EM-035: Rol de tutor, PR #76](https://github.com/Alexis01000011/EngiMods/pull/76).
- Catálogo multi-juego, permisos diferenciados y documentación técnica.

**Guion — Fabián:** «En EM-010 trabajé el catálogo para representar cada juego como dato, sin limitar la plataforma a uno solo. En EM-011 añadí versiones, entornos y compatibilidades. Esto permite indicar con qué combinación se probó el contenido. En EM-035 trabajé el rol de tutor: no es lo mismo ser tutor que administrador, y las pantallas de tutoría comprueban permisos. También preparé la documentación técnica y las evidencias.»

**Evidencia:** [PR #75](https://github.com/Alexis01000011/EngiMods/pull/75), [PR #79](https://github.com/Alexis01000011/EngiMods/pull/79), [PR #76](https://github.com/Alexis01000011/EngiMods/pull/76), [PR #77](https://github.com/Alexis01000011/EngiMods/pull/77), [PR #117](https://github.com/Alexis01000011/EngiMods/pull/117).

---

## Diapositiva 10 — Aportaciones de Alexis

- Implementó la mayoría del ciclo de Misión Cero: registro, pago, inscripción, lecciones, entregas y revisión.
- 39 commits y la mayor parte de los PRs integrados.
- Configuró CI, staging, identidad visual y el plan de contenido.

**Guion — Alexis:** (Alexis prepara su guion con sus historias y PRs principales.)

**Evidencia:** Los PRs están en el [repositorio](https://github.com/Alexis01000011/EngiMods/pulls?q=is%3Apr+is%3Amerged).

---

## Diapositiva 11 — Plan de marketing

- **Mensaje:** «Aprende a construir tu propio mod con una ruta en español y versiones claras.»
- **Canales:** comunidades de Discord, YouTube, Reddit, recomendaciones.
- **Costo de validación:** MXN 0 (difusión orgánica); MXN 1,500 de reserva para pauta si es necesario.
- **Piloto en una semana:** acordar condiciones → preparar pieza de difusión → difundir → observar → decidir.

**Notas:** No se ha lanzado ninguna campaña. El plan de marketing es para después de que el recorrido esté listo y los textos legales estén publicados. Las métricas del piloto ya están instrumentadas en la plataforma (EM-091).

---

## Diapositiva 12 — Métricas y decisiones

| Indicador | Qué mide | Si es bajo |
|---|---|---|
| Comprensión | ¿Entienden la oferta? | Aclarar el mensaje |
| Interés por juego | ¿Qué juego quieren? | Priorizar contenido |
| Conversión | ¿Se inscriben? | Revisar precio o recorrido |
| Finalización | ¿Terminan? | Revisar dificultad y soporte |
| Tiempo de revisión | ¿Se revisa en 24 h? | Ajustar capacidad |

**Notas:** Estos indicadores se definen antes del piloto con umbrales y ventanas acordadas por el equipo. Sin datos reales no se calculan; se presentan como el plan de medición.

---

## Diapositiva 13 — Próximos pasos

1. Publicar textos legales y abrir el registro.
2. Cargar contenido de Misión Cero para Minecraft y probarlo en el juego.
3. Configurar correo real cuando se retome EM-008.
4. Lanzar el piloto: difundir, medir y decidir.
5. Si la validación es positiva: implementar el curso de seis semanas con grupos.

**Notas:** La entrega de semestre demuestra la plataforma construida y el modelo de negocio. Los próximos pasos requieren decisiones del equipo (legales, contenido, correo). El proyecto se diseñó para operarse de verdad.

---

## Material visual sugerido

| Captura | Qué demuestra |
|---|---|
| Landing y catálogo de juegos | Propuesta de valor visible al visitante |
| Detalle del curso con precio | Información clara antes del pago |
| Pantalla de lección con "Probado con" | Diferenciador de versión probada |
| Panel del alumno con avance | Experiencia de aprendizaje |
| Cola de revisión del tutor | Retroalimentación real |
| Métricas del piloto (admin) | Instrumentación lista |

Las capturas se toman de staging con datos de prueba identificados. No se presentan como evidencia de alumnos reales.
