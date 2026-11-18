---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "1. Antes de empezar"
orden: 1
titulo: Qué vas a construir y cómo se trabaja aquí
minutos: 10
estado: borrador sin probar
---

<!-- Contenido de la lección: copia desde aquí -->

En esta Misión Cero vas a crear un mod para Minecraft: Java Edition. Es pequeño, pero lo vas a construir como se construye software en un equipo: con Git, con pruebas automáticas y con un README que dice con qué versión funciona. En esta lección ves el mapa completo antes de instalar nada.

## Al terminar podrás

- Explicar qué hace el mod que vas a construir.
- Distinguir un mod de Fabric de un *datapack*.
- Leer el sello "Probado con" de cada lección.
- Decir qué vas a entregar al final y cómo se revisa.

## Necesitas

Nada todavía. Solo 10 minutos y ganas de leer con calma.

## Lo que vas a construir

Un comando para el chat del juego que tira dados. Escribes cuántos dados quieres y cuántas caras tiene cada uno, y el mod te dice qué salió:

```text
/dado 2d6     →  2d6: 3 + 5 = 8
/dado d20     →  1d20: 17
/dado         →  1d6: 4
/dado 0d6     →  Puedes tirar de 1 a 20 dados a la vez.
```

`2d6` se lee "dos dados de seis caras". Es la forma de escribir tiradas que usan muchos juegos de mesa y de rol.

Parece poco, pero tiene lo mismo que un mod grande: leer lo que escribe el jugador, revisar que tenga sentido, hacer un cálculo, responder en el juego y avisar con claridad cuando algo está mal.

## Mod, *datapack* y Fabric

Minecraft: Java Edition se puede cambiar de dos formas:

- **Un *datapack*** son archivos de datos (JSON y funciones de comandos) que el juego lee sin instalar nada. Puede cambiar recetas, botines o avances, pero solo puede hacer lo que el juego ya permite.
- **Un mod** es código en Java que corre dentro del juego. Puede agregar comportamiento nuevo, como un comando que el juego no trae.

Para que el juego cargue un mod hace falta un *loader*. Aquí usas **Fabric**, que tiene dos piezas:

- **Fabric Loader** carga tu mod cuando arranca el juego.
- **Fabric API** es una biblioteca con puntos de entrada listos, por ejemplo para registrar comandos.

Fabric es ligero, tiene documentación oficial y, desde la versión 26.1 del juego, usa los mismos nombres de clases que el código de Mojang. `[VERIFICAR: que desde 26.1 Fabric use los nombres oficiales de Mojang, en el blog oficial de Fabric]`

## Cómo está armado tu mod

Tu mod tiene dos partes, y separarlas es la idea más importante de esta Misión Cero:

```text
┌───────────────────────────────┐      ┌──────────────────────────────┐
│ Núcleo (Java puro)            │      │ Adaptador (Fabric)           │
│ Lee "2d6", valida y tira      │ ←─── │ Registra /dado y responde    │
│ Se prueba sin abrir el juego  │      │ en el chat                   │
└───────────────────────────────┘      └──────────────────────────────┘
```

- **El núcleo** no sabe que existe Minecraft. Lo compruebas con pruebas automáticas en segundos.
- **El adaptador** es una clase pequeña que conecta el núcleo con el juego.

Cuando salga una versión nueva de Minecraft, lo más probable es que solo tengas que tocar el adaptador. El núcleo y sus pruebas siguen igual.

## El sello "Probado con"

Arriba de cada lección hay un sello con la versión del juego y de Fabric con la que se probó, y la fecha. Usa exactamente esas versiones. Minecraft cambia seguido, y un paso que funciona en una versión puede fallar en otra.

> ※ Si una lección dice "Sin versión probada", todavía no se ha comprobado. Avísale a tu tutor antes de seguirla.

## Cómo se trabaja aquí

- Son 7 lecciones en 3 módulos, unas 4 horas en total. Avanzas a tu ritmo durante los días de acceso que dice la página del curso.
- Cada lección termina con un *commit*: un punto guardado de tu proyecto en Git.
- Al final hay un solo ejercicio: entregas el enlace a tu repositorio en GitHub.
- Un tutor revisa tu entrega con una rúbrica de cinco criterios: que funcione en la versión que declaras, que la lógica tenga pruebas que pasen, cómo usaste Git, que tu README esté completo y que hagas lo que pide el ejercicio. Si algo falta, te dice qué cambiar y puedes volver a enviar.

## Si algo falla

Esta lección no tiene pasos técnicos. Si no ves el sello "Probado con" arriba de las lecciones o no puedes abrir la siguiente, escríbele a tu tutor.

## Cómo lo haría un equipo

Antes de escribir código, un equipo acuerda qué significa "terminado". Aquí ya lo sabes: tu mod está terminado cuando cumple los cinco criterios de la rúbrica. Tenlos a la vista mientras avanzas; en la lección 7 los usas para revisarte antes de enviar.

## Guarda tu avance

Todavía no hay nada que guardar en Git. Marca esta lección como completada y sigue con **Prepara tu laboratorio**, donde instalas Java, Git y el editor.
