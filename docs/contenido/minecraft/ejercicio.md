---
curso: Misión Cero: tu primer mod para Minecraft
leccion: Documenta y entrega (módulo 3, lección 1)
titulo: "Tu primer mod: el comando /dado"
estado: borrador sin probar
---

# Ejercicio y rúbrica

Se captura en el admin como el `Exercise` de la lección **Documenta y entrega**, con sus cinco `RubricCriterion`.

## Instrucciones (`Exercise.instructions`)

<!-- Instrucciones del ejercicio: copia desde aquí hasta la sección "Rúbrica" -->

Entrega tu mod `/dado` funcionando, con su núcleo probado, su historia en Git y su README.

### Punto de partida

Tu repositorio de las lecciones anteriores: el proyecto de Fabric con el paquete `core` (la lógica del dado y sus pruebas) y el paquete `fabric` (el comando).

### Qué debe hacer tu mod

- `/dado` tira un dado de 6 caras.
- `/dado 2d6` tira los dados que diga la tirada y muestra cada valor y el total.
- Una tirada que no se entiende o que está fuera de los límites (de 1 a 20 dados, de 2 a 100 caras) muestra en rojo un mensaje que dice cómo corregirla.

### Pasos

1. Termina las lecciones 5, 6 y 7.
2. Corre las pruebas con `./gradlew test`. **Comprueba:** pasan todas.
3. Arranca el juego con `./gradlew runClient` y prueba la tabla de la lección **Conecta el núcleo al juego**. **Comprueba:** cada caso responde como dice la tabla.
4. Completa tu README y tu licencia, y declara la versión `0.1.0`.
5. Crea y sube la etiqueta `v0.1.0`. **Comprueba:** aparece en la pestaña **Tags** de tu repositorio.

### Qué entregar

- **Enlace al repositorio Git:** tu repositorio público, por ejemplo `https://github.com/tuusuario/dado`.
- **Versión del juego** y **entorno de modding:** los que usaste.
- **Comentario:** di que tu entrega es la etiqueta `v0.1.0` (o la que corresponda si reenvías) y, en dos o tres frases, qué decisión tomaste tú o qué fue lo más difícil.

### Cómo se revisa

Tu tutor clona tu repositorio en la etiqueta que indicas y revisa cinco criterios:

1. **Funciona en la versión declarada:** compila y el comando responde en el juego como pide el ejercicio.
2. **La lógica tiene pruebas y pasan:** las pruebas del núcleo pasan y el núcleo no depende de Minecraft.
3. **Uso de Git:** *commits* pequeños con mensajes claros, sin archivos generados.
4. **README:** cualquiera puede entender, compilar y usar tu mod sin preguntarte.
5. **Alcance:** hace lo que pide el ejercicio y puedes explicar tu código.

Si algo falta, tu tutor te dice qué cambiar en cada criterio. Corrige, crea una etiqueta nueva (`v0.1.1`) y vuelve a enviar.

### Antes de enviar

- `./gradlew test` pasa.
- `/dado 2d6`, `/dado` y `/dado 0d6` responden como en la tabla.
- En el repositorio no hay `build/`, `run/` ni archivos `.jar`.
- El README tiene las versiones con las que probaste.
- Existe `LICENSE` con tu nombre.
- La etiqueta está subida a GitHub.

## Rúbrica (`RubricCriterion`)

| Orden | Criterio | Qué se revisa |
|---|---|---|
| 1 | Funciona en la versión declarada | El proyecto compila en la etiqueta entregada con las versiones de `gradle.properties`. Con `runClient`, `/dado 2d6` muestra cada valor y el total; `/dado` tira 1d6; `/dado 0d6` y `/dado hola` muestran en rojo un mensaje que dice cómo corregir la tirada. La versión del juego y del entorno de la entrega coinciden con las del proyecto y el README. |
| 2 | La lógica tiene pruebas y pasan | `./gradlew test` pasa. Hay pruebas para tiradas válidas, textos que no son tiradas, límites (0 y 21 dados, 1 y 101 caras), el rango de los valores, que salgan todas las caras y el mensaje. Nada en el paquete `core` importa `net.minecraft` ni `net.fabricmc`. |
| 3 | Uso de Git | Además del *commit* de la plantilla hay varios *commits* propios, uno por paso, con mensajes que dicen qué cambió. El repositorio no contiene `build/`, `run/`, `.gradle/`, `.idea/` ni archivos `.jar`. Existe la etiqueta indicada en el comentario. |
| 4 | README | Dice qué hace el mod, cómo se usa (con ejemplos), con qué versiones de Minecraft, Fabric Loader, Fabric API y Java se probó, cómo se corren las pruebas y el juego, y cuál es la licencia. Existe `LICENSE` y coincide con `fabric.mod.json`. |
| 5 | Alcance | El mod hace lo que pide el ejercicio. El comentario de la entrega explica una decisión propia o una dificultad con palabras del alumno. No hay código que no tenga que ver con el ejercicio ni partes que el alumno no pueda explicar. |

`[VERIFICAR con el equipo: si el criterio 5 debe pedir una explicación más formal (por ejemplo, en el README) para que el tutor pueda revisarlo sin una llamada.]`
