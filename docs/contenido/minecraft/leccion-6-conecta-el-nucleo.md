---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "2. Tu primer mod"
orden: 4
titulo: Conecta el núcleo al juego
minutos: 40
estado: borrador sin probar
---

<!-- Contenido de la lección: copia desde aquí -->

Tu lógica ya funciona y está probada. Ahora la conectas con Minecraft: registras el comando `/dado`, le pasas al núcleo lo que escribió el jugador y respondes en el chat. Todo lo que sabe de Minecraft va a vivir en una sola clase pequeña, el adaptador.

## Al terminar podrás

- Registrar un comando de chat con Fabric API.
- Leer un argumento del comando y pasárselo a tu núcleo.
- Responder en el chat con el resultado o con un mensaje de error.
- Explicar por qué el adaptador debe ser pequeño.

## Necesitas

- La lección **El núcleo: la lógica del dado con pruebas** completa, con las 19 pruebas en verde.

## Cómo funciona un comando

Minecraft lee los comandos con **Brigadier**, una biblioteca de Mojang. Un comando es un árbol:

```text
dado                  →  tira 1d6
└── <tirada>          →  tira lo que diga la tirada, por ejemplo 2d6
```

Cada rama dice qué texto acepta y qué hacer cuando el comando termina ahí. Fabric API te avisa cuando el juego está listo para registrar comandos, con el evento `CommandRegistrationCallback`.

## 1. Escribe el adaptador

Crea el paquete `io.github.tuusuario.dado.fabric`, al lado de `core`. El nombre dice qué es: la parte que conecta con Fabric.

En `src/main/java/io/github/tuusuario/dado/fabric/DadoCommand.java`:

```java
package io.github.tuusuario.dado.fabric;

import com.mojang.brigadier.Command;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import io.github.tuusuario.dado.core.DiceRoll;
import io.github.tuusuario.dado.core.RollResult;
import java.util.concurrent.ThreadLocalRandom;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;

/** Conecta el comando /dado del juego con la lógica del núcleo. */
public final class DadoCommand {

    private DadoCommand() {
    }

    public static void register() {
        CommandRegistrationCallback.EVENT.register((dispatcher, registryAccess, environment) ->
                dispatcher.register(Commands.literal("dado")
                        .executes(context -> roll(context, "1d6"))
                        .then(Commands.argument("tirada", StringArgumentType.word())
                                .executes(context -> roll(
                                        context, StringArgumentType.getString(context, "tirada"))))));
    }

    private static int roll(CommandContext<CommandSourceStack> context, String text) {
        CommandSourceStack source = context.getSource();
        try {
            RollResult result = DiceRoll.parse(text).roll(ThreadLocalRandom.current());
            source.sendSuccess(() -> Component.literal(result.message()), false);
            return Command.SINGLE_SUCCESS;
        } catch (IllegalArgumentException e) {
            source.sendFailure(Component.literal(e.getMessage()));
            return 0;
        }
    }
}
```

`[VERIFICAR: compilar contra Minecraft 26.3 y Fabric API. En particular: el paquete de CommandRegistrationCallback (v2), los nombres oficiales Commands, CommandSourceStack y Component, y las firmas de sendSuccess y sendFailure.]`

Qué hace cada parte:

- **`Commands.literal("dado")`** es la raíz del árbol: la palabra que escribe el jugador.
- **`.executes(...)` en la raíz** dice qué pasa con `/dado` solo: tira `1d6`.
- **`Commands.argument("tirada", StringArgumentType.word())`** acepta una palabra después de `/dado`. `word()` acepta letras, números y algunos signos, así que `2d6` pasa entero.
- **`roll(...)`** es todo el trabajo del adaptador: le da el texto al núcleo, toma el resultado y lo manda al chat. No sabe nada de dados.
- **`ThreadLocalRandom.current()`** es el generador de azar de verdad. Es un `RandomGenerator`, así que el núcleo lo acepta igual que el `Random` con semilla de tus pruebas.
- **`sendSuccess`** responde al jugador que escribió el comando. El `false` indica que no se avise a los administradores del servidor.
- **`sendFailure`** muestra el mensaje en rojo. El texto es el que escribiste en el núcleo: dice qué hacer.
- **`Command.SINGLE_SUCCESS`** (vale 1) le dice al juego que el comando salió bien; `0`, que no.

## 2. Regístralo al cargar el mod

Abre la clase principal de tu mod y agrega una línea en `onInitialize()`, después del mensaje del registro:

```java
@Override
public void onInitialize() {
    LOGGER.info("Dado cargado. Escribe /dado en el chat.");
    DadoCommand.register();
}
```

IntelliJ IDEA marca `DadoCommand` en rojo hasta que agregues su `import`: pon el cursor encima y presiona <kbd>Alt</kbd> + <kbd>Enter</kbd> (<kbd>Option</kbd> + <kbd>Enter</kbd> en macOS) › **Import class**.

**Comprueba:** corre `./gradlew build` (o `.\gradlew build`). Termina con `BUILD SUCCESSFUL`. `build` también corre tus pruebas: siguen pasando las 19.

## 3. Pruébalo en el juego

1. Arranca el juego con **runClient**, como en la lección **Ejecuta el juego con tu mod**.
2. Entra a tu mundo `Pruebas`.
3. Presiona <kbd>T</kbd> y escribe `/da`.

**Comprueba:** el chat te sugiere `/dado`. Si escribes `/dado ` (con espacio), te muestra `<tirada>`.

4. Prueba cada caso de esta tabla y marca lo que ves:

| Escribe | Debes ver |
|---|---|
| `/dado 2d6` | `2d6:` con dos valores, su suma y el total, por ejemplo `2d6: 3 + 5 = 8` |
| `/dado` | `1d6:` y un número del 1 al 6 |
| `/dado d20` | `1d20:` y un número del 1 al 20 |
| `/dado 0d6` | En rojo: `Puedes tirar de 1 a 20 dados a la vez.` |
| `/dado 2d1` | En rojo: `Un dado puede tener de 2 a 100 caras.` |
| `/dado hola` | En rojo: `Escribe la tirada como 2d6: cuántos dados, una d y cuántas caras.` |

`[VERIFICAR: que los comandos sin requires(...) se puedan usar en un mundo sin trucos activados]`

5. Cierra el juego con **Guardar y salir al título** y **Salir del juego**.

> ※ Si el comando falla con un error que no es tuyo (por ejemplo, el chat dice "Ocurrió un error inesperado"), busca `dado` en el registro. La línea del error dice en qué clase y en qué línea pasó.

## Si algo falla

`[VERIFICAR: completar con los errores encontrados en la prueba real. Abajo, los más probables; quitar los que no aparezcan.]`

- **No compila: `cannot find symbol` en `CommandRegistrationCallback`, `Commands` o `Component`:** los nombres de las clases cambian entre versiones de Minecraft y de Fabric API. Revisa que tus versiones sean las del sello "Probado con". Si lo son, avísale a tu tutor: esta lección necesita revalidarse.
- **El chat dice `Comando desconocido`:** el comando no se registró. Revisa que `DadoCommand.register()` esté dentro de `onInitialize()` y que en el registro aparezca tu mensaje de carga.
- **`/dado 2d6` funciona pero `/dado` solo no:** falta el `.executes(...)` de la raíz, antes del `.then(...)`.

## Cómo lo haría un equipo

- **Un adaptador pequeño.** `DadoCommand` traduce: texto del juego al núcleo y resultado del núcleo al chat. No decide nada. Cuando salga Minecraft 26.4 y cambie algo de esta API, solo tocas esta clase; tu lógica y sus 19 pruebas siguen igual.
- **El mismo núcleo, otro juego.** En la Misión Cero de Hytale, el núcleo es el mismo y solo cambia el adaptador. Así se ve en la práctica que la lógica de tu mod no es del juego.
- **Probar a mano lo que no se prueba solo.** La tabla del paso 3 es una prueba manual: siempre los mismos casos, siempre el mismo resultado esperado. En la lección 7 la vas a poner en tu README para que cualquiera la repita.

## Guarda tu avance

```text
git add .
git commit -m "Registra el comando /dado y lo conecta con el núcleo"
git push
```

**Comprueba:** en GitHub ves el paquete `fabric` con `DadoCommand.java`. En la siguiente lección, **Documenta y entrega**, preparas tu mod para que otra persona lo entienda y lo use, y lo envías a revisión.
