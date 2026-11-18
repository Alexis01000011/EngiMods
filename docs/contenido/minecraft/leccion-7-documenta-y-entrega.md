---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "3. Entrega"
orden: 1
titulo: Documenta y entrega
minutos: 30
estado: borrador sin probar
ejercicio: ver ejercicio.md
---

<!-- Contenido de la lección: copia desde aquí -->

Tu mod funciona. Ahora lo dejas listo para que otra persona lo entienda, lo compile y lo use sin preguntarte nada: un README, una licencia, una versión y una etiqueta en Git. Al final envías tu entrega y tu tutor la revisa.

## Al terminar podrás

- Escribir un README que diga qué hace tu mod, cómo se usa y con qué versión funciona.
- Elegir una licencia para tu código.
- Marcar la versión `0.1.0` de tu mod con una etiqueta de Git.
- Enviar tu entrega y saber cómo se revisa.

## Necesitas

- La lección **Conecta el núcleo al juego** completa: `/dado` funciona en el juego y las 19 pruebas pasan.

## 1. Escribe tu README

El README es lo primero que ve quien abre tu repositorio. Crea el archivo `README.md` en la raíz del proyecto (al lado de `build.gradle`) y usa esta base. Cambia lo que está entre corchetes:

~~~markdown
# Dado

Mod de Minecraft: Java Edition que agrega el comando `/dado` para tirar dados en el chat.

## Uso

| Comando | Qué hace |
|---|---|
| `/dado` | Tira un dado de 6 caras. |
| `/dado 2d6` | Tira 2 dados de 6 caras y muestra cada valor y el total. |
| `/dado d20` | Tira un dado de 20 caras. |

Se pueden tirar de 1 a 20 dados, de 2 a 100 caras cada uno.

## Versiones

Probado con:

- Minecraft: Java Edition 26.3
- Fabric Loader [versión de tu gradle.properties]
- Fabric API [versión de tu gradle.properties]
- Java 25

## Instalación

1. Instala Fabric Loader para Minecraft 26.3.
2. Copia `dado-0.1.0.jar` y Fabric API en la carpeta `mods` de tu Minecraft.

## Desarrollo

```text
./gradlew test        corre las pruebas del núcleo
./gradlew runClient   arranca el juego con el mod
./gradlew build       genera el .jar en build/libs/
```

La lógica está en `core` (Java puro, con pruebas) y la conexión con el juego en `fabric`.

### Prueba manual

| Escribe | Debes ver |
|---|---|
| `/dado 2d6` | Dos valores, su suma y el total |
| `/dado 0d6` | En rojo: "Puedes tirar de 1 a 20 dados a la vez." |
| `/dado hola` | En rojo: cómo escribir una tirada |

## Licencia

MIT. Ver `LICENSE`.

No es un mod oficial de Minecraft. No está aprobado por Mojang ni por Microsoft ni está asociado con ellos.
~~~

`[VERIFICAR: texto del aviso según las Usage Guidelines vigentes de Minecraft]`

**Comprueba:** en IntelliJ IDEA, abre `README.md` y usa la vista previa (botón arriba a la derecha del editor). Las tablas y los títulos se ven bien y las versiones son las de tu `gradle.properties`.

## 2. Elige una licencia

Sin licencia, nadie más puede usar ni modificar tu código legalmente, aunque esté público. Para un mod pequeño y abierto, la licencia **MIT** es la más simple: cualquiera puede usarlo si conserva tu nombre y la licencia.

1. Abre `https://choosealicense.com/licenses/mit/` y copia el texto.
2. Pégalo en un archivo `LICENSE` en la raíz del proyecto. Si la plantilla ya trajo uno, reemplaza su contenido. `[VERIFICAR: si la plantilla de Fabric incluye LICENSE y con qué licencia]`
3. Cambia `[year]` por el año y `[fullname]` por tu nombre.
4. En `src/main/resources/fabric.mod.json`, cambia el campo `license` a `"MIT"`.

**Comprueba:** `LICENSE` tiene tu nombre y el año, y `fabric.mod.json` dice `"license": "MIT"`.

> ※ Puedes elegir otra licencia si la entiendes. Lo que no puede faltar es que tu repositorio diga cuál es.

## 3. Declara la versión

Tu mod tiene su propia versión, distinta de la del juego. Usa **versionado semántico**: `MAYOR.MENOR.PARCHE`. Empiezas en `0.1.0`: la primera versión que funciona, todavía en desarrollo.

En `gradle.properties`, cambia la línea de la versión del mod:

```properties
mod_version=0.1.0
```

`[VERIFICAR: nombre de la propiedad en la plantilla de 26.3 y que fabric.mod.json tome la versión de ahí con ${version}]`

Abre `fabric.mod.json` y revisa el bloque `depends`. Dice con qué versión de Minecraft, Fabric Loader y Fabric API funciona tu mod; la plantilla ya lo llenó con las versiones de tu proyecto.

**Comprueba:** `depends` menciona `minecraft` con `26.3`. `[VERIFICAR: formato que pone la plantilla, por ejemplo "~26.3"]`

## 4. Genera el .jar

Corre:

- Windows (PowerShell): `.\gradlew build`
- macOS, Linux o Git Bash: `./gradlew build`

**Comprueba:** termina con `BUILD SUCCESSFUL` y en `build/libs/` aparece `dado-0.1.0.jar`. Ese archivo es tu mod: es lo que alguien copiaría a su carpeta `mods`. `[VERIFICAR: nombre exacto del .jar que genera la plantilla]`

> ※ El `.jar` no se sube al repositorio: se puede generar de nuevo en cualquier momento con `build`.

## 5. Revísate antes de enviar

Estos son los cinco criterios con los que te revisa tu tutor. Revisa cada uno:

- **Funciona en la versión declarada.** Arrancas con `runClient` y `/dado 2d6`, `/dado` y `/dado 0d6` responden como en la tabla de la lección anterior.
- **La lógica tiene pruebas y pasan.** `./gradlew test` pasa y en `core` no hay nada de `net.minecraft` ni de `net.fabricmc`.
- **Uso de Git.** Tienes un *commit* por cada paso de las lecciones, con mensajes que dicen qué cambió. En el repositorio no hay `build/`, `run/` ni `.jar`.
- **README completo.** Dice qué hace el mod, cómo se usa, con qué versiones se probó, cómo se compila y cuál es la licencia.
- **Alcance.** Tu mod hace lo que pide el ejercicio y puedes explicar cada parte de tu código.

## 6. Guarda y marca la versión

Guarda tus cambios:

```text
git add .
git commit -m "Documenta el mod y declara la versión 0.1.0"
git push
```

Ahora crea una **etiqueta** (*tag*): un nombre fijo para este *commit*. Tu tutor va a revisar exactamente lo que marque la etiqueta, aunque después sigas cambiando cosas.

```text
git tag -a v0.1.0 -m "Primera versión: comando /dado"
git push origin v0.1.0
```

**Comprueba:** en GitHub, abre el selector de ramas de tu repositorio y la pestaña **Tags**. Aparece `v0.1.0`.

<details>
<summary>Opcional: publica el .jar como versión de GitHub</summary>
<p>En tu repositorio, entra a <strong>Releases › Draft a new release</strong>, elige la etiqueta <code>v0.1.0</code>, escribe en dos líneas qué trae esta versión y adjunta <code>build/libs/dado-0.1.0.jar</code>. Así cualquiera descarga tu mod sin compilarlo. No es parte de la entrega.</p>
</details>

## 7. Envía tu entrega

Al final de esta lección está el ejercicio **Tu primer mod: el comando /dado**. Toca **Ver instrucciones y enviar mi entrega** y llena el formulario:

- **Enlace al repositorio Git:** la dirección de tu repositorio, por ejemplo `https://github.com/tuusuario/dado`.
- **Versión del juego:** 26.3.
- **Entorno de modding:** Fabric, con la versión del sello "Probado con".
- **Comentario:** di que tu entrega es la etiqueta `v0.1.0` y, en dos o tres frases, qué decisión tomaste tú o qué fue lo más difícil.

Toca **Enviar mi entrega**.

**Comprueba:** tu entrega aparece como **Enviada**. Cuando tu tutor la tome, cambia a **En revisión**.

Si tu tutor pide cambios, verás cada criterio con su comentario. Haz los cambios, súbelos, crea una etiqueta nueva (`v0.1.1`) y vuelve a enviar desde la misma pantalla. Tus envíos anteriores y sus revisiones se guardan.

## Si algo falla

`[VERIFICAR: completar con los errores encontrados en la prueba real. Abajo, los más probables; quitar los que no aparezcan.]`

- **`git push origin v0.1.0` dice que la etiqueta ya existe:** ya la habías subido. Si necesitas corregir algo, no la muevas: crea `v0.1.1`.
- **`build` falla en la tarea `test`:** alguna prueba se rompió con tus últimos cambios. Abre `build/reports/tests/test/index.html` para ver cuál.
- **El formulario no acepta tu enlace:** debe ser la dirección pública del repositorio en GitHub, GitLab, Bitbucket o Codeberg, empezando con `https://`. Revisa que el repositorio sea público.

## Cómo lo haría un equipo

- **El README es un contrato.** Dice qué promete tu mod y con qué versiones. Si alguien tiene un problema con otra versión, el README ya le dijo que no estaba probado ahí.
- **Las etiquetas no se mueven.** `v0.1.0` siempre señala lo mismo. Si corriges algo, sale `v0.1.1`. Así cualquiera puede volver a una versión exacta.
- **Revisarse antes de pedir revisión.** La lista del paso 5 te ahorra una ronda con tu tutor.

## Guarda tu avance

Ya subiste tu *commit* y tu etiqueta. Marca esta lección como completada y espera la revisión de tu tutor.

Terminaste tu primer mod: un núcleo con pruebas, un adaptador pequeño, historia en Git, un README y una versión. Con eso ya trabajas como se trabaja en un proyecto de software, aunque el mod sea pequeño.
