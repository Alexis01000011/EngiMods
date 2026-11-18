# Misión Cero para Minecraft: borradores

Borradores del contenido de *Misión Cero: tu primer mod para Minecraft*, escritos con el plan de `docs/contenido/plan-hytale-minecraft.md`. Este es contenido de pago; el equipo decidió guardarlo en este repositorio público (decisión D5 del plan).

**Estado: borrador sin probar.** Ninguna lección se ha seguido de punta a punta con el juego. No registres su `LessonTest` ni las publiques hasta que pasen la prueba real y la revisión por pares (plan, sección 9). Cada dato que falta confirmar está marcado con `[VERIFICAR: ...]`. Antes de cargar una lección en el admin, resuelve todos sus `[VERIFICAR]`: no deben llegar a la plataforma.

## Decisiones aplicadas

Las tomó el equipo el 17/11/2026:

| Decisión | Valor |
|---|---|
| D1. Juego que va primero | Minecraft: Java Edition |
| D2. Entorno | Fabric |
| D4. Proyecto | Comando `/dado` |
| D5. Dónde vive el contenido | `docs/contenido/minecraft/` en este repositorio, que es público |
| D6. Precio y acceso | MXN 199 y 30 días de acceso |
| D9. Título | Misión Cero: tu primer mod para Minecraft |

Siguen abiertas: D3 (tipo de mod de Hytale), D7 (quién prueba cada juego) y D8 (dónde viven los repositorios plantilla). También sigue abierto si el precio incluye IVA (`docs/BACKLOG.md`, sección final).

## Archivos

| Archivo | Qué es |
|---|---|
| `leccion-1-que-vas-a-construir.md` … `leccion-7-documenta-y-entrega.md` | Una lección por archivo. Arriba vienen los datos para el admin; abajo, el contenido en Markdown. |
| `ejercicio.md` | Ejercicio de la lección 7 y su rúbrica |
| `guia-de-prueba.md` | Qué hace y qué anota quien prueba cada lección |

## Datos para el admin

Captúralos en este orden: primero el catálogo y después el curso.

### Juego (`Game`)

| Campo | Valor |
|---|---|
| Nombre | Minecraft: Java Edition |
| Slug | `minecraft-java` |
| Descripción corta | La edición de Minecraft para computadora que admite mods en Java. Aquí aprendes a crearlos con Fabric. |
| Sitio oficial | `https://www.minecraft.net/` |
| URL del logo | Vacío (`DESIGN.md` no usa arte de los juegos) |
| Estado | El que corresponda al publicar el curso |

### Versión del juego (`GameVersion`)

| Campo | Valor |
|---|---|
| Número | `26.3` |
| Fecha de publicación | 15/09/2026 `[VERIFICAR: fecha oficial de la 26.3]` |
| Es la actual | Sí |

### Entorno de modding (`ModdingEnvironment`)

| Campo | Valor |
|---|---|
| Nombre | Fabric |
| Versión | `Loader 0.19.5 · API 0.161.0+26.3` `[VERIFICAR: versiones en fabricmc.net y en Modrinth; registrar las que se usen en la prueba]` |
| Versiones compatibles | 26.3 |

### Curso (`Course`)

| Campo | Valor |
|---|---|
| Título | Misión Cero: tu primer mod para Minecraft |
| Slug | `mision-cero-minecraft` |
| Juego | Minecraft: Java Edition |
| Tipo | Práctica corta |
| Nivel | Principiante |
| Duración en semanas | 1 |
| Precio en centavos | `19900` (MXN 199) |
| Días de acceso | 30 |
| Estado | Borrador hasta que todas las lecciones estén probadas |

**Descripción:**

```text
Crea tu primer mod para Minecraft: Java Edition con Fabric: un comando /dado que tira dados y muestra el resultado en el chat. Lo construyes como se construye software: la lógica en Java con pruebas automáticas, el proyecto en Git y GitHub, y un README que dice con qué versión funciona. Al final entregas tu repositorio y un tutor lo revisa con una rúbrica de cinco criterios. Son 7 lecciones, unas 4 horas en total, a tu ritmo.

EngiMods no es un producto oficial de Minecraft. No está aprobado por Mojang ni por Microsoft ni está asociado con ellos.
```

`[VERIFICAR: el aviso sigue las Usage Guidelines vigentes de Minecraft. Confirmar el texto exacto en la fuente oficial, si debe ir también en inglés ("NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.") y si el título cumple las reglas de uso del nombre.]`

**Requisitos:**

```text
- Una computadora con Windows 10 u 11, macOS o Linux, con al menos 8 GB de RAM y 10 GB libres.
- Minecraft: Java Edition comprado.
- Programación básica: variables, condicionales, ciclos y funciones en cualquier lenguaje. No necesitas saber Java ni Git; los vas usando paso a paso.
- Una cuenta de GitHub (la creas en la lección 2 si no la tienes).
```

`[VERIFICAR: RAM y espacio con la prueba real.]`

### Módulos y lecciones

| Módulo (orden) | Lección (orden) | Archivo | Minutos |
|---|---|---|---|
| 1. Antes de empezar | 1. Qué vas a construir y cómo se trabaja aquí | `leccion-1-que-vas-a-construir.md` | 10 |
| | 2. Prepara tu laboratorio | `leccion-2-prepara-tu-laboratorio.md` | 40 |
| 2. Tu primer mod | 1. Crea tu proyecto | `leccion-3-crea-tu-proyecto.md` | 30 |
| | 2. Ejecuta el juego con tu mod | `leccion-4-ejecuta-el-juego.md` | 20 |
| | 3. El núcleo: la lógica del dado con pruebas | `leccion-5-el-nucleo-con-pruebas.md` | 45 |
| | 4. Conecta el núcleo al juego | `leccion-6-conecta-el-nucleo.md` | 40 |
| 3. Entrega | 1. Documenta y entrega | `leccion-7-documenta-y-entrega.md` | 30 |

Total estimado: 215 minutos. Los minutos se ajustan con el tiempo medido en la prueba real.

Cada lección se captura con su título y su contenido. El contenido es todo lo que viene después de la línea `<!-- Contenido de la lección: copia desde aquí -->`; no copies los datos de arriba. Carga la lección en borrador; publícala solo después de registrar su `LessonTest`.

## Versiones que usan las lecciones

| Herramienta | Versión | Estado |
|---|---|---|
| Minecraft: Java Edition | 26.3 | `[VERIFICAR]` en el plan, sección 7 |
| Fabric Loader | 0.19.5 | `[VERIFICAR]` |
| Fabric API | 0.161.0+26.3 | `[VERIFICAR]`: hay reportes de 0.162.0 |
| Fabric Loom | 1.17 | `[VERIFICAR]` |
| Gradle (wrapper) | 9.6.0 | `[VERIFICAR]` |
| Java (JDK) | 25 | `[VERIFICAR]` |
| JUnit | 6.1.3 | Comprobado en Maven Central el 17/11/2026 |

El 17/11/2026 la red de la sesión que escribió estos borradores bloqueó `fabricmc.net`, `docs.fabricmc.net`, `maven.fabricmc.net` y `minecraft.net`. Por eso ningún dato de Fabric ni de Mojang se volvió a confirmar.

## Qué se comprobó y qué no

- **Sí:** el núcleo de la lección 5 (`DiceRoll`, `RollResult` y sus 19 pruebas) se compiló y se probó con JUnit 6.1.3 y Java 21 el 17/11/2026. Pasaron las 19 pruebas. Con el error a propósito de la lección, falla solo `everyFaceCanComeUp`, como dice la lección.
- **No:** nada que dependa de Fabric o de Minecraft (plantilla, `build.gradle`, `runClient`, el adaptador de la lección 6, el `.jar`). Es lo primero que revisa la prueba real (`guia-de-prueba.md`).
