# Guía de prueba: Misión Cero para Minecraft

Para la persona del equipo que prueba las lecciones antes de publicarlas (plan, sección 9). La prueba es lo que convierte un borrador en una lección "Probado con". Sin ella, la lección no se publica.

## Antes de empezar

- **Máquina limpia.** De preferencia Windows 11, que es lo más común en el público, sin Java ni el proyecto instalados de antes. Si usas tu máquina de siempre, anota qué ya tenías instalado.
- **Sigue la lección tal cual.** Lee como alumno: si un paso te obliga a adivinar, eso es un hallazgo, aunque sepas resolverlo.
- **Usa un repositorio nuevo** en tu cuenta de GitHub. Bórralo al terminar o déjalo como ejemplo para tutores.
- **Ten a la mano** esta guía, un cronómetro y un archivo de notas.

## Qué anotar en toda la prueba

Copia esta tabla en tus notas y llénala:

| Dato | Valor |
|---|---|
| Fecha de la prueba | |
| Sistema operativo y versión | |
| Procesador, RAM y espacio libre | |
| Versión de Minecraft (`gradle.properties`) | |
| Fabric Loader | |
| Fabric API | |
| Loom (`build.gradle`) | |
| Gradle (`gradle/wrapper/gradle-wrapper.properties`) | |
| Java (`java -version`) | |
| IntelliJ IDEA | |

Por cada lección anota:

- **Minutos reales,** de principio a fin, sin contar pausas.
- **Cada error:** el texto exacto (copia las líneas del registro), en qué paso salió y cómo lo resolviste.
- **Cada paso confuso:** dónde dudaste y qué te faltó saber.
- **Cada `[VERIFICAR]`:** el dato real que encontraste, con la fuente oficial y la fecha.

## Por lección

### 1. Qué vas a construir y cómo se trabaja aquí

- [ ] El ejemplo de salida coincide con lo que realmente muestra el mod al final (lección 6).
- [ ] Lo que dice de Fabric y los nombres de Mojang es correcto según el blog oficial de Fabric.

### 2. Prepara tu laboratorio

- [ ] La descarga recomendada de Temurin 25 existe con ese nombre y las opciones del instalador se llaman como dice la lección.
- [ ] `java -version` muestra 25 en una terminal nueva.
- [ ] La forma de descargar IntelliJ IDEA gratis es la que dice la lección.
- [ ] Anota cuánto espacio y cuánta descarga hicieron falta (para los requisitos del curso).

### 3. Crea tu proyecto

- [ ] El generador de plantillas ofrece Minecraft 26.3 y los campos se llaman como en la tabla.
- [ ] Anota qué opciones avanzadas hay y cuáles conviene dejar sin marcar.
- [ ] Anota cuánto tardó la primera sincronización de Gradle.
- [ ] Los nombres de las propiedades de `gradle.properties` coinciden con la lección.
- [ ] `fabric.mod.json` trae `description`, `authors` y `license`.
- [ ] El `.gitignore` excluye `build/`, `.gradle/`, `run/` y `.idea/`.
- [ ] Anota si el generador incluye `LICENSE` y cuál.
- [ ] Al final hay dos *commits* en GitHub.

### 4. Ejecuta el juego con tu mod

- [ ] La plantilla trae `LOGGER` y la línea `Hello Fabric world!` (o anota qué trae).
- [ ] Anota dónde está `runClient` en el panel Gradle.
- [ ] Copia la línea exacta del registro que lista los mods cargados y la versión inicial del mod.
- [ ] El juego no pide iniciar sesión en el entorno de desarrollo.
- [ ] `run/logs/latest.log` existe y trae el mensaje.

### 5. El núcleo: la lógica del dado con pruebas

- [ ] `build.gradle` está en Groovy y no traía un bloque `test`.
- [ ] JUnit 6.1.3 funciona junto con Loom (o anota la versión que funcionó).
- [ ] La primera prueba falla por compilación, como dice la lección.
- [ ] Los conteos del reporte son 14, 18 y 19 en los pasos 4, 5 y 6.
- [ ] Con el error a propósito falla solo `everyFaceCanComeUp`.

### 6. Conecta el núcleo al juego

Esta es la lección con más riesgo: su código no se ha compilado contra Minecraft 26.3.

- [ ] `DadoCommand` compila sin cambios. Si no, anota cada cambio necesario (paquete, clase o firma) y corrige la lección.
- [ ] Cada fila de la tabla del paso 3 responde como dice la lección.
- [ ] El comando funciona en un mundo sin trucos activados.
- [ ] El autocompletado sugiere `/dado` y `<tirada>`.

### 7. Documenta y entrega

- [ ] El nombre de la propiedad de versión y el formato de `depends` coinciden con la lección.
- [ ] El `.jar` se llama `dado-0.1.0.jar`.
- [ ] La etiqueta `v0.1.0` aparece en GitHub.
- [ ] Haz una entrega de prueba en staging con un usuario de prueba y revísala con la rúbrica desde la cuenta de tutor.
- [ ] Opcional: instala el `.jar` y Fabric API en tu Minecraft normal y comprueba `/dado` fuera del entorno de desarrollo.

## Al terminar

1. Corrige las lecciones con lo que encontraste: resuelve cada `[VERIFICAR]`, llena "Si algo falla" con los errores reales (quita los que no salieron) y ajusta los minutos.
2. Actualiza las versiones en `README.md` de esta carpeta y en el plan (sección 7) si cambiaron.
3. Pide a otra persona la revisión por pares con la lista del plan (sección 9).
4. Captura en el admin el juego, la versión, el entorno, el curso, los módulos, las lecciones, el ejercicio y su rúbrica, todo en borrador.
5. Registra un `LessonTest` por lección con la versión del juego, el entorno y la **fecha de tu prueba**.
6. Publica las lecciones y después el curso.
