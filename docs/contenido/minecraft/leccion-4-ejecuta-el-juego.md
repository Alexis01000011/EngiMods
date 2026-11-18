---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "2. Tu primer mod"
orden: 2
titulo: Ejecuta el juego con tu mod
minutos: 20
estado: borrador sin probar
---

<!-- Contenido de la lección: copia desde aquí -->

Antes de agregar algo nuevo, comprueba que lo que ya tienes funciona: tu proyecto debe arrancar Minecraft y el juego debe cargar tu mod. En esta lección lo arrancas desde IntelliJ IDEA y aprendes a leer el registro (*log*), que es la primera herramienta para entender qué pasa dentro del juego.

## Al terminar podrás

- Arrancar Minecraft con tu mod desde el proyecto.
- Encontrar en el registro la línea que confirma que tu mod cargó.
- Escribir un mensaje propio en el registro.
- Saber dónde quedan los registros para revisarlos después.

## Necesitas

- La lección **Crea tu proyecto** completa, con el proyecto abierto en IntelliJ IDEA y sincronizado.

## 1. Escribe tu mensaje en el registro

Abre la clase principal de tu mod (la que dice `implements ModInitializer`). La plantilla ya trae un `LOGGER` y una línea en `onInitialize()` parecida a esta:

```java
LOGGER.info("Hello Fabric world!");
```

Cámbiala por un mensaje tuyo:

```java
LOGGER.info("Dado cargado. Escribe /dado en el chat.");
```

`[VERIFICAR: que la plantilla de 26.3 traiga LOGGER y esa línea en onInitialize()]`

> ※ Usa el `LOGGER` y no `System.out.println`. El registro dice la hora, de qué mod viene cada línea y si es información, una advertencia o un error.

## 2. Arranca el juego

Tienes dos formas; usa la que te acomode:

- **Desde el panel Gradle** (a la derecha): abre **Tasks › fabric** y haz doble clic en **runClient**. `[VERIFICAR: grupo de la tarea runClient en el panel Gradle]`
- **Desde la terminal** de IntelliJ IDEA:
  - Windows (PowerShell): `.\gradlew runClient`
  - macOS, Linux o Git Bash: `./gradlew runClient`

La primera vez tarda unos minutos más en preparar el juego. Abajo, en la ventana **Run**, vas viendo el registro.

**Comprueba:** en el registro aparece una línea parecida a `Loading 70 mods:` con una lista en la que está `dado 1.0.0`. Unas líneas después aparece tu mensaje: `Dado cargado. Escribe /dado en el chat.` `[VERIFICAR: texto exacto de la línea del Loader y la versión inicial que pone la plantilla]`

> ※ Para buscar en el registro, haz clic dentro de la ventana **Run** y presiona <kbd>Ctrl</kbd> + <kbd>F</kbd> (<kbd>Cmd</kbd> + <kbd>F</kbd> en macOS). Busca `dado`.

## 3. Entra a un mundo

Se abre una ventana de Minecraft. En el entorno de desarrollo el juego no te pide iniciar sesión: entras con un nombre de prueba como `Player123`.

1. Elige **Un jugador › Crear mundo nuevo**.
2. Ponle de nombre `Pruebas`, elige el modo **Creativo** y crea el mundo.

**Comprueba:** entras al mundo y puedes moverte. Si presionas <kbd>T</kbd> se abre el chat.

> ※ Este mundo vive en la carpeta `run/` de tu proyecto, no en tu Minecraft de siempre. Puedes romper lo que quieras.

## 4. Cierra el juego bien

Presiona <kbd>Esc</kbd> y elige **Guardar y salir al título** y después **Salir del juego**.

**Comprueba:** en IntelliJ IDEA, la ventana **Run** dice que el proceso terminó (`Process finished` o `BUILD SUCCESSFUL`).

> ※ Si detienes el juego con el botón rojo de IntelliJ IDEA, el mundo puede no guardarse. Úsalo solo si el juego se congela.

## 5. Encuentra el registro guardado

Lo que viste en la ventana **Run** también queda en un archivo: `run/logs/latest.log`. Ábrelo desde el panel del proyecto en IntelliJ IDEA.

**Comprueba:** encuentras tu mensaje en `latest.log`. Los registros de arranques anteriores quedan comprimidos en la misma carpeta.

## Si algo falla

`[VERIFICAR: completar con los errores encontrados en la prueba real. Abajo, los más probables; quitar los que no aparezcan.]`

- **El juego se cierra al arrancar y el registro menciona `Incompatible mods` o una versión de Fabric API:** las versiones de `gradle.properties` no coinciden con las de la lección. Compáralas con el sello "Probado con", corrígelas y vuelve a sincronizar Gradle.
- **La ventana del juego queda en negro o se cierra sin mensaje:** actualiza el controlador de tu tarjeta de video y vuelve a intentar.
- **El registro dice `OutOfMemoryError`:** cierra otros programas pesados, como el navegador con muchas pestañas, y vuelve a arrancar.

Si el error no está en esta lista, copia las 20 líneas anteriores al primer `ERROR` del registro. Es lo primero que te va a pedir tu tutor.

## Cómo lo haría un equipo

- **Probar lo que ya hay antes de cambiar algo.** Si arrancas ahora y funciona, cualquier error de la siguiente lección viene de lo que agregues tú, no de la instalación.
- **El registro es la primera fuente de información.** Un buen mensaje dice qué pasó y de qué parte viene. Un equipo no adivina por qué falló algo: lee el registro.

## Guarda tu avance

Primero revisa qué cambió:

```text
git status
```

**Comprueba:** aparece solo la clase principal. Si aparece la carpeta `run/`, revisa tu `.gitignore` antes de seguir.

Guarda tu cambio y súbelo:

```text
git add .
git commit -m "Muestra un mensaje al cargar el mod"
git push
```

En la siguiente lección, **El núcleo: la lógica del dado con pruebas**, escribes la parte más importante de tu mod sin abrir el juego.
