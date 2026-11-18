---
modulo: 1
orden: 1
titulo: Qué vas a construir
minutos: 10
estado: borrador conceptual
---

<!-- Contenido de la lección: copia desde aquí -->

¿Qué pasaría si pudieras tirar dados sin salir del chat? Diseñaremos un plugin de servidor para recibir `/dado 2d6`, calcular dos valores y mostrar su suma. Primero aprenderás a comprobar la lógica sin abrir el juego; la conexión real todavía requiere una versión y prueba verificadas.

## Al terminar podrás

- Explicar el proyecto y distinguir el núcleo del adaptador.
- Interpretar `2d6` y reconocer una entrada inválida.
- Identificar qué significa «Probado con» y qué se entrega.

## Necesitas

Curiosidad y conocimientos básicos de variables, condiciones y funciones. Para esta muestra no necesitas instalar nada.

## 1. Lee una tirada

En `2d6`, el primer número es la cantidad de dados y el último, las caras de cada uno. La letra `d` los separa. Por ejemplo, una respuesta posible sería `2d6: [3, 5] = 8`; otra tirada puede ser diferente. **Comprueba:** los dos valores están entre 1 y 6 y 3 + 5 es 8.

Prueba en papel: ¿qué significa `d20`? Es un dado de 20 caras: si no escribes cantidad, usamos uno. ¿Y `0d6`? Lo rechazamos porque exigiremos de 1 a 20 dados y de 2 a 100 caras. **Comprueba:** `2d101` también se rechaza.

## 2. Separa las piezas

El **núcleo** recibe el texto, valida límites, genera valores y prepara un mensaje. El **adaptador** recibe el comando del servidor, pide el resultado al núcleo y lo devuelve al jugador. Una prueba Java puede revisar el núcleo sin Hytale; solo una prueba en juego demuestra la conexión.

Un plugin de servidor ejecuta código Java; un paquete de recursos modifica datos o contenido sin necesitar programación. La documentación oficial describe la segunda ruta en [Crear contenido](https://docs.hytale.com/creating-content/). Aquí proponemos la primera.

## 3. Lee las señales de calidad

«Probado con» significa que alguien siguió esa lección en una versión concreta del juego y entorno y registró la fecha. Una versión mostrada en una página oficial no demuestra que el curso se haya probado. Si ves «Sin versión probada», no supongas que la integración funciona.

Al final proponemos entregar un repositorio público y una etiqueta de Git para que un tutor revise exactamente el código, las pruebas y la documentación. **Comprueba:** puedes nombrar un dato que requiere prueba real: que `/dado` responda en el chat.

## Si algo falla

Si `2d6` te confunde, dibuja dos dados con seis caras y suma dos valores posibles. Si el total de ejemplo fuera 9, revisa la suma: 3 + 5 es 8. Estas son orientaciones didácticas, no errores observados en una prueba de alumnos.

## Cómo lo haría un equipo

Un equipo separa reglas del juego y conexión para probar cada parte por separado; registra lo que sí verificó y lo que todavía desconoce.

## Guarda tu avance

Anota en una hoja una entrada válida, una inválida y la diferencia entre núcleo y adaptador. Si ya usas Git, guarda tus notas con un commit `Explica el proyecto del dado`; no es obligatorio instalar Git para esta muestra. Sigue con **Prepara tu laboratorio** cuando la práctica esté habilitada.
