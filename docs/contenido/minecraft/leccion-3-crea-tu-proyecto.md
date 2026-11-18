---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "2. Tu primer mod"
orden: 1
titulo: Crea tu proyecto
minutos: 30
estado: borrador sin probar
---

<!-- Contenido de la lección: copia desde aquí -->

Un mod de Fabric empieza con un proyecto de Gradle que ya sabe descargar Minecraft, compilar tu código y arrancar el juego. En esta lección lo creas con el generador oficial de Fabric, conoces sus archivos y lo subes a GitHub con tu primer *commit*.

## Al terminar podrás

- Crear un proyecto de mod con el generador de plantillas de Fabric.
- Abrirlo en IntelliJ IDEA con Java 25.
- Explicar para qué sirve cada archivo importante.
- Subir tu proyecto a un repositorio de GitHub con *commits* pequeños.

## Necesitas

- La lección **Prepara tu laboratorio** completa: Java 25, Git, IntelliJ IDEA y tu cuenta de GitHub.
- Tu nombre de usuario de GitHub a la mano.

## 1. Genera el proyecto

1. Entra a `https://fabricmc.net/develop/template/`.
2. Llena el formulario así:

| Campo | Escribe | Por qué |
|---|---|---|
| Mod Name | `Dado` | Es el nombre que ven los jugadores. |
| Mod ID | `dado` | Identifica tu mod dentro del juego. Solo minúsculas, números, `-` y `_`. |
| Package Name | `io.github.tuusuario.dado` | Cambia `tuusuario` por tu usuario de GitHub en minúsculas. Si tiene guiones, cámbialos por `_`: Java no acepta guiones en paquetes. |
| Minecraft Version | `26.3` | La versión con la que se probó esta lección. |

3. En las opciones avanzadas deja **Kotlin** y **Data Generation** sin marcar: no los usas. `[VERIFICAR: nombres de las opciones avanzadas del generador y si conviene desmarcar "Split client and common sources"]`
4. Descarga el `.zip` y descomprímelo en una carpeta corta, sin espacios ni acentos, por ejemplo `C:\mods\dado` en Windows o `~/mods/dado` en macOS y Linux.

> ※ No pongas el proyecto dentro de una carpeta sincronizada con OneDrive, iCloud o Dropbox. La sincronización bloquea archivos mientras Gradle trabaja y provoca errores difíciles de entender.

**Comprueba:** dentro de la carpeta ves `build.gradle`, `gradle.properties`, `gradlew`, `gradlew.bat` y la carpeta `src`.

## 2. Ábrelo en IntelliJ IDEA

1. En IntelliJ IDEA elige **Open** y selecciona la carpeta del proyecto (la que tiene `build.gradle`).
2. Si te pregunta si confías en el proyecto, elige **Trust Project**.
3. IntelliJ IDEA detecta Gradle y empieza a sincronizar. La primera vez descarga Gradle, Minecraft y Fabric: puede tardar de 5 a 15 minutos. `[VERIFICAR: tiempo real]` Mira el avance en la barra de abajo.
4. Revisa que use Java 25:
    - **File › Project Structure › Project › SDK:** elige `25` (Temurin).
    - **Settings › Build, Execution, Deployment › Build Tools › Gradle › Gradle JVM:** elige también `25`.

**Comprueba:** abre la ventana **Build** (abajo). La sincronización termina sin mensajes en rojo, y en el panel **Gradle** (a la derecha) aparecen las tareas del proyecto.

## 3. Conoce tu proyecto

No necesitas entender cada línea hoy. Sí necesitas saber dónde está cada cosa.

| Archivo o carpeta | Para qué sirve |
|---|---|
| `gradle.properties` | Las versiones del proyecto: Minecraft, Fabric Loader, Fabric API y la versión de tu mod. |
| `build.gradle` | Las instrucciones para compilar tu mod. Usa el plugin **Loom** de Fabric, que descarga Minecraft y prepara el juego para desarrollo. |
| `settings.gradle` | El nombre del proyecto y de dónde se descargan los plugins. |
| `gradlew`, `gradlew.bat` y `gradle/wrapper/` | El *wrapper* de Gradle: descarga la versión exacta de Gradle que pide el proyecto. Por eso no instalaste Gradle. |
| `src/main/java/io/github/tuusuario/dado/` | Tu código. Ya trae la clase principal del mod. |
| `src/main/resources/fabric.mod.json` | La ficha del mod: su ID, nombre, versión, autores, de qué depende y qué clase arranca primero. |
| `src/main/resources/assets/dado/` | Recursos del mod, como su ícono. |
| `.gitignore` | Lo que Git no debe guardar: archivos generados, la carpeta del juego de prueba y la configuración local del editor. |

Ahora abre `gradle.properties`.

**Comprueba:** dice `minecraft_version=26.3` y las versiones de Fabric Loader y Fabric API coinciden con el sello "Probado con" de esta lección. `[VERIFICAR: nombres exactos de las propiedades en la plantilla de 26.3, por ejemplo loader_version y fabric_version o fabric_api_version]`

Después abre la clase principal en `src/main/java/io/github/tuusuario/dado/`. Es la que dice `implements ModInitializer`. Su método `onInitialize()` es lo primero de tu código que corre cuando el juego carga el mod.

## 4. Haz tu primer *commit*

Abre la terminal de IntelliJ IDEA (**View › Tool Windows › Terminal**). Ya está en la carpeta del proyecto.

1. Crea el repositorio. Si el generador ya lo creó, Git te lo dice y no pasa nada:

```text
git init
```

2. Revisa qué va a guardar Git:

```text
git status
```

**Comprueba:** aparecen `src/`, `build.gradle` y los demás archivos del proyecto, pero no aparecen `build/`, `.gradle/`, `run/` ni `.idea/`. Esas carpetas se generan en tu computadora y no van en el repositorio. `[VERIFICAR: que el .gitignore de la plantilla excluya esas cuatro carpetas]`

3. Guarda todo en tu primer *commit*:

```text
git add .
git commit -m "Crea el proyecto desde la plantilla de Fabric"
```

## 5. Súbelo a GitHub

1. En GitHub, toca **New repository** (botón **+** arriba a la derecha).
2. Nómbralo `dado`, déjalo **Public** y **no marques** README, `.gitignore` ni licencia. El repositorio debe quedar vacío; si no, Git no te deja subir tu proyecto.
3. Copia la dirección que te da GitHub y conéctala con tu proyecto:

```text
git remote add origin https://github.com/tuusuario/dado.git
git push -u origin main
```

La primera vez se abre una ventana para entrar a GitHub. Acepta.

**Comprueba:** recarga la página de tu repositorio en GitHub. Ves tus archivos y tu *commit* "Crea el proyecto desde la plantilla de Fabric".

## 6. Pon tus datos en la ficha del mod

Abre `src/main/resources/fabric.mod.json` y cambia dos campos:

```json
"description": "Comando /dado para tirar dados en el chat.",
"authors": [
  "Tu Nombre"
],
```

Deja lo demás como está. `[VERIFICAR: que la plantilla traiga los campos description y authors]`

**Comprueba:** IntelliJ IDEA no marca el archivo en rojo. Un error de JSON, como una coma de más, se ve subrayado.

Guarda el cambio en su propio *commit* y súbelo:

```text
git add src/main/resources/fabric.mod.json
git commit -m "Agrega la descripción y el autor del mod"
git push
```

**Comprueba:** en GitHub ves dos *commits*.

## Si algo falla

`[VERIFICAR: completar con los errores encontrados en la prueba real. Abajo, los más probables; quitar los que no aparezcan.]`

- **La sincronización de Gradle falla con `Unsupported class file major version` o pide otra versión de Java:** la **Gradle JVM** no es la 25. Cámbiala en el paso 2 y sincroniza de nuevo con el botón de recargar del panel **Gradle**.
- **La descarga se detiene o falla por tiempo:** vuelve a sincronizar. Gradle reanuda lo que ya bajó.
- **`git push` dice `rejected` o `fetch first`:** el repositorio de GitHub no estaba vacío. Lo más simple es borrarlo (**Settings › Danger Zone**), crearlo de nuevo sin marcar nada y repetir el paso 5.
- **`git push` dice `src refspec main does not match any`:** tu rama no se llama `main`. Revisa el paso 4 de **Prepara tu laboratorio** y cambia el nombre con `git branch -M main`.

## Cómo lo haría un equipo

- **Versiones fijas.** `gradle.properties` y el *wrapper* fijan las versiones exactas. Cualquier persona que clone tu repositorio compila con las mismas, incluido tu tutor.
- **El primer *commit* es la plantilla sin cambios.** Así, más adelante puedes comparar y ver exactamente qué escribiste tú y qué venía de Fabric.
- **Lo generado no se guarda.** `build/` y `run/` se pueden volver a crear en cualquier momento; guardarlas solo llena el repositorio de ruido.

## Guarda tu avance

Ya tienes dos *commits* en GitHub: la plantilla tal como vino y tus datos. En la siguiente lección, **Ejecuta el juego con tu mod**, arrancas Minecraft con tu proyecto por primera vez.
