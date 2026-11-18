---
modulo: 1
orden: 2
titulo: Prepara tu laboratorio
minutos: 40
estado: borrador sin prueba del juego
---

<!-- Contenido de la lección: copia desde aquí -->

Prepararás herramientas para escribir y probar Java. La integración con Hytale aún no se probó en un servidor: no confundas tener Java listo con tener un plugin funcionando.

## Al terminar podrás

- Identificar JDK, Git y una carpeta de trabajo.
- Comprobar las versiones instaladas y localizar los archivos oficiales del servidor.
- Reconocer qué información nunca debes compartir.

## Necesitas

Una computadora con conexión a internet, permiso de instalación y programación básica. Para la fase en juego necesitas Hytale con acceso legítimo y una cuenta; no se requiere para L5. El [manual oficial](https://support.hytale.com/hc/en-us/articles/45326769420827-Hytale-Server-Manual) indica Java 25 y al menos 4 GB de memoria para el servidor, no para servidor y cliente a la vez.

## 1. Instala y revisa Java

1. Descarga un **JDK 25** desde [Adoptium](https://adoptium.net/temurin/releases/) u otra distribución confiable; el JDK incluye compilador. Completa el instalador para tu sistema y abre una terminal nueva.
2. Escribe:

```text
java --version
javac --version
```

**Comprueba:** ambos comandos muestran la versión 25. Anota la versión completa y el sistema operativo; si solo funciona `java`, falta el compilador o la terminal no encuentra el JDK.

## 2. Prepara Git y editor

1. Instala [Git](https://git-scm.com/downloads), abre otra terminal y ejecuta `git --version`. **Comprueba:** aparece un número de versión.
2. Usa un editor de texto o IDE de Java; por ejemplo [IntelliJ IDEA](https://www.jetbrains.com/idea/download/). Crea una carpeta `dado` propia, fuera de la instalación del juego. **Comprueba:** puedes crear y guardar ahí un archivo de texto.
3. Para entregar más tarde necesitarás un repositorio público en GitHub, GitLab, Bitbucket o Codeberg. No pegues contraseñas ni tokens en archivos ni capturas.

## 3. Localiza el servidor sin publicarlo

Consulta la sección **Server Files** del manual oficial. Explica cómo copiar `Server` y `Assets.zip` desde una instalación legítima. No subas esos archivos ni el mundo, las credenciales o configuraciones al repositorio. **Comprueba:** sabes dónde están, sin moverlos todavía. Si no tienes el juego, puedes continuar con el núcleo de L5; registra la integración como pendiente.

## Si algo falla

Orientaciones preventivas, no incidencias observadas: si `javac` no existe, instala un JDK y abre una terminal nueva; revisa la ruta del ejecutable. Si una versión difiere, anótala y consulta al tutor antes de hacer afirmaciones de compatibilidad. Si faltan archivos del launcher, consulta el manual oficial y no los descargues de fuentes no autorizadas.

## Cómo lo haría un equipo

Registra el entorno para que otra persona pueda repetir la prueba. La versión de Java no sustituye la versión de juego ni la de la API.

## Guarda tu avance

Escribe en tus notas sistema operativo y versiones, sin datos privados. En L3 crearás el repositorio y tu primer commit.
