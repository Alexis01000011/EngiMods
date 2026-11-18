---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "1. Antes de empezar"
orden: 2
titulo: Prepara tu laboratorio
minutos: 40
estado: borrador sin probar
---

<!-- Contenido de la lección: copia desde aquí -->

Antes de escribir tu mod necesitas cuatro herramientas: Java, Git, una cuenta de GitHub y un editor. En esta lección instalas cada una y compruebas que funciona, para que en las siguientes lecciones no te detenga la instalación.

## Al terminar podrás

- Comprobar que tienes Java 25, Git e IntelliJ IDEA instalados.
- Configurar Git con tu nombre y tu correo.
- Entrar a tu cuenta de GitHub.
- Abrir una terminal y saber qué versión de cada herramienta tienes.

## Necesitas

- Una computadora con Windows 10 u 11, macOS o Linux, con al menos 8 GB de RAM y 10 GB libres. `[VERIFICAR: con la prueba real]`
- Conexión a internet: vas a descargar cerca de 2 GB entre herramientas y archivos del juego. `[VERIFICAR: tamaño real]`
- Permiso para instalar programas en esa computadora.

> ※ Si ya tienes alguna de estas herramientas, no la reinstales: haz solo su paso "Comprueba". Si la versión no coincide, entonces sí sigue el paso completo.

## Abre una terminal

Vas a usar la terminal para comprobar cada instalación.

- **Windows:** abre el menú Inicio y escribe `PowerShell`. Después de instalar Git (paso 2) también tendrás **Git Bash**; cualquiera de las dos sirve.
- **macOS:** abre la app **Terminal** (en Aplicaciones › Utilidades).
- **Linux:** abre la terminal de tu escritorio.

> ※ Cada vez que instales algo, cierra la terminal y abre una nueva. Una terminal que ya estaba abierta no se entera de lo que acabas de instalar.

## 1. Instala Java 25

Minecraft 26.3 y Fabric necesitan el **JDK** de Java 25 (el kit para programar, no solo el que corre programas). `[VERIFICAR: versión mínima de Java para desarrollar mods de Fabric en 26.3]`

1. Entra a `https://adoptium.net/` y descarga **Eclipse Temurin 25 (LTS)** para tu sistema. `[VERIFICAR: que Temurin 25 sea la descarga recomendada en adoptium.net]`
2. Instálalo con las opciones de siempre. En Windows, en el instalador, marca **Set JAVA_HOME variable** y **Add to PATH**. `[VERIFICAR: nombres de las opciones en el instalador .msi]`
3. Abre una terminal nueva y escribe:

```text
java -version
```

**Comprueba:** la primera línea dice `25` (por ejemplo, `openjdk version "25.0.1"`).

## 2. Instala Git

Git guarda la historia de tu proyecto: cada cambio, quién lo hizo y por qué.

1. Descárgalo de `https://git-scm.com/downloads`.
    - **Windows:** instala **Git for Windows** con las opciones que trae marcadas. Incluye Git Bash y Git Credential Manager, que guarda tu inicio de sesión de GitHub.
    - **macOS:** al escribir `git --version` en la terminal, el sistema ofrece instalar las herramientas de Xcode, que traen Git. Acepta.
    - **Linux:** instálalo con el gestor de paquetes de tu distribución, por ejemplo `sudo apt install git`.
2. En una terminal nueva escribe:

```text
git --version
```

**Comprueba:** aparece `git version` y un número.

## 3. Crea tu cuenta de GitHub

GitHub guarda tu repositorio en internet. Ahí lo va a ver tu tutor.

1. Entra a `https://github.com/` y crea una cuenta, o entra con la que ya tienes.
2. Elige un nombre de usuario que no te dé pena enseñar: va a aparecer en la dirección de tu mod.
3. Activa la verificación en dos pasos en **Settings › Password and authentication**.
4. Busca tu correo privado de GitHub en **Settings › Emails**: tiene la forma `12345678+tuusuario@users.noreply.github.com`. Úsalo en Git para no publicar tu correo personal en cada *commit*.

**Comprueba:** puedes entrar a `https://github.com/tuusuario` y ves tu perfil.

## 4. Configura Git

Cada *commit* lleva un nombre y un correo. Configúralos una sola vez:

```text
git config --global user.name "Tu Nombre"
git config --global user.email "12345678+tuusuario@users.noreply.github.com"
git config --global init.defaultBranch main
```

Cambia el nombre y el correo por los tuyos. La tercera línea hace que tus repositorios nuevos empiecen en la rama `main`, igual que en GitHub.

**Comprueba:**

```text
git config --global --list
```

Aparecen `user.name`, `user.email` e `init.defaultbranch=main` con tus datos.

## 5. Instala IntelliJ IDEA

IntelliJ IDEA es el editor que usan la mayoría de quienes hacen mods en Java: entiende Gradle, te avisa de errores mientras escribes y corre el juego con un clic.

1. Descárgalo de `https://www.jetbrains.com/idea/download/`.
2. Instálalo con las opciones de siempre y ábrelo.

Las funciones que usas en esta Misión Cero son gratuitas; no necesitas suscripción. `[VERIFICAR: cómo se distribuye hoy la versión gratuita de IntelliJ IDEA (desde 2025.3 hay una sola descarga) y qué funciones quedan gratis]`

**Comprueba:** IntelliJ IDEA abre y muestra la pantalla de bienvenida con **New Project** y **Open**.

<details>
<summary>Opcional: plugin Minecraft Development</summary>
<p>En <strong>Settings › Plugins</strong> puedes instalar <strong>Minecraft Development</strong>. Ayuda a leer los archivos de los mods, pero esta Misión Cero no lo necesita. <code>[VERIFICAR: que funcione con Minecraft 26.3]</code></p>
</details>

## 6. Comprueba tu Minecraft

Para esta Misión Cero no abres el juego desde el launcher: Fabric lo arranca desde el proyecto. Aun así necesitas Minecraft: Java Edition comprado para jugar con tu mod fuera del editor.

**Comprueba:** puedes entrar al Minecraft Launcher con tu cuenta y ves **Minecraft: Java Edition** en la lista de juegos.

## Si algo falla

`[VERIFICAR: completar con los errores encontrados en la prueba real. Abajo, los más probables; quitar los que no aparezcan.]`

- **`java` no se reconoce como comando:** primero cierra la terminal y abre una nueva. Si sigue igual, Java no quedó en el `PATH`. En Windows, vuelve a correr el instalador y marca **Add to PATH**.
- **`java -version` dice 17 o 21:** tienes otra versión de Java antes en el `PATH`. En Windows, revisa **Variables de entorno**: `JAVA_HOME` debe apuntar a la carpeta de Temurin 25 y `%JAVA_HOME%\bin` debe ir antes que otras rutas de Java.
- **GitHub no te deja crear la cuenta con ese usuario:** ya existe. Prueba con otro; no tiene que ser tu nombre real.

## Cómo lo haría un equipo

En un equipo todos usan las mismas versiones de las herramientas. Así se evita el clásico "en mi máquina sí funciona". Por eso cada lección dice con qué versión se probó y por qué en la lección 7 vas a escribir tus versiones en el README.

## Guarda tu avance

Todavía no tienes repositorio. Anota en un lugar a la mano la versión de Java (`java -version`) y de Git (`git --version`) que te salieron: las vas a escribir en tu README. Marca esta lección como completada y sigue con **Crea tu proyecto**.
