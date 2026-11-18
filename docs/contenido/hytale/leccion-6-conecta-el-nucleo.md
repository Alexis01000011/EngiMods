---
modulo: 2
orden: 4
titulo: Conecta el núcleo
minutos: 40
estado: adaptador compilado y JAR revisado; falta la prueba en servidor y juego
---

<!-- Contenido de la lección: copia desde aquí -->

El núcleo ya tiene una prueba propia. Ahora escribirás el adaptador que recibe `/dado`, llama al núcleo y devuelve el resultado al chat. El ejemplo se compila contra el JAR oficial del servidor 0.7.7 y se empaqueta con su manifiesto. **La carga en un servidor y la respuesta en el juego todavía no se han probado**; esta lección separa lo que ya puedes compilar de lo que aún debes observar.

## Al terminar podrás

- Explicar cómo el adaptador traduce el comando al núcleo.
- Compilar el plugin contra el JAR del servidor y armar un JAR con `manifest.json`.
- Revisar el contenido del JAR antes de copiarlo a `mods/`.
- Preparar la prueba en un servidor aislado sin abrir puertos.

## Necesitas

- L5 terminada: `Pruebas del núcleo: OK`.
- JDK 25 y Git de L2.
- El `manifest.json` de L3 en la raíz de `dado`.
- Una copia legítima del JAR del servidor 0.7.7, **fuera del repositorio**. En el ejemplo se usó el artefacto oficial `Server-0.7.7.jar`; no lo subas a Git.
- Para la prueba final: Hytale con acceso legítimo, una cuenta y un servidor local aislado. La versión exacta del cliente se confirma al registrar la prueba.

## 1. Define el contrato

El adaptador es delgado: no repite los límites del núcleo ni suma valores. Solo traduce.

| Entrada | Qué hace el adaptador | Respuesta esperada |
|---|---|---|
| `/dado` | Usa `1d6` | Un valor de 1 a 6 y su total. |
| `/dado 2d6` | Pasa `2d6` a `Dice.parse` | Dos valores y su suma. |
| `/dado d20` | Pasa `d20` | Un valor de 1 a 20. |
| `/dado 0d6` | El núcleo lanza `IllegalArgumentException` | Mensaje que pide entre 1 y 20 dados. |
| `/dado 2d1` | El núcleo lanza `IllegalArgumentException` | Mensaje que pide entre 2 y 100 caras. |
| `/dado hola` | El núcleo lanza `IllegalArgumentException` | Mensaje que propone `2d6`. |
| `/dado 2d6 extra` | No ejecuta una tirada parcial | Instrucción de uso. |

Dos reglas de diseño:

1. Un error de entrada se muestra como mensaje al emisor, **sin apagar el servidor ni imprimir un stacktrace**.
2. El comando no exige permisos de administrador. Cualquier jugador puede tirar dados; el adaptador llama `requireNoPermission()`.

## 2. Escribe el punto de entrada

Crea `src/curso/dado/hytale/DadoPlugin.java`:

```java
package curso.dado.hytale;

import com.hypixel.hytale.server.core.plugin.JavaPlugin;
import com.hypixel.hytale.server.core.plugin.JavaPluginInit;

/** Punto de entrada del plugin: registra el comando una vez al cargar. */
public final class DadoPlugin extends JavaPlugin {
    public DadoPlugin(JavaPluginInit init) {
        super(init);
    }

    @Override
    protected void setup() {
        getCommandRegistry().registerCommand(new DadoCommand());
    }
}
```

`JavaPluginInit` conecta el plugin con el servidor. `setup()` es donde registras el comando. No escribas un `main`: el servidor construye esta clase.

**Comprueba:** el paquete es `curso.dado.hytale`, la clase es pública, tiene el constructor `DadoPlugin(JavaPluginInit)` y extiende `JavaPlugin`.

## 3. Escribe el adaptador

Crea `src/curso/dado/hytale/DadoCommand.java`:

```java
package curso.dado.hytale;

import com.hypixel.hytale.server.core.Message;
import com.hypixel.hytale.server.core.command.system.CommandContext;
import com.hypixel.hytale.server.core.command.system.arguments.system.RequiredArg;
import com.hypixel.hytale.server.core.command.system.arguments.types.ArgTypes;
import com.hypixel.hytale.server.core.command.system.basecommands.CommandBase;
import curso.dado.Dice;
import java.util.Random;

/** Adaptador mínimo: traduce el comando al núcleo y devuelve el mensaje al emisor. */
public final class DadoCommand extends CommandBase {
    private static final String USO = "Uso: /dado [tirada], por ejemplo /dado 2d6";

    public DadoCommand() {
        super("dado", "Tira dados con notación como 2d6");
        // La línea con demasiados argumentos llega aquí para responder con una instrucción.
        setAllowsExtraArguments(true);
        requireNoPermission();
        addUsageVariant(new WithRoll());
    }

    @Override
    protected void executeSync(CommandContext context) {
        if (!argumentsAfterCommand(context.getInputString()).isEmpty()) {
            context.sendMessage(Message.raw(USO));
            return;
        }
        respond(context, "1d6");
    }

    private static void respond(CommandContext context, String input) {
        try {
            Dice dice = Dice.parse(input);
            context.sendMessage(Message.raw(dice.message(dice.roll(new Random()))));
        } catch (IllegalArgumentException error) {
            context.sendMessage(Message.raw(error.getMessage()));
        }
    }

    /** Devuelve el texto posterior al nombre del comando; vacío si no hay argumentos. */
    static String argumentsAfterCommand(String input) {
        if (input == null) {
            return "";
        }
        int space = input.indexOf(' ');
        return space < 0 ? "" : input.substring(space + 1).trim();
    }

    private static final class WithRoll extends CommandBase {
        private final RequiredArg<String> roll =
                withRequiredArg("tirada", "Tirada como 2d6", ArgTypes.STRING);

        private WithRoll() {
            super("Tira dados con la tirada indicada");
            requireNoPermission();
        }

        @Override
        protected void executeSync(CommandContext context) {
            respond(context, context.get(roll));
        }
    }
}
```

Qué hace cada pieza:

- `CommandBase("dado", ...)` declara el nombre y la descripción del comando.
- `WithRoll` es una variante para exactamente una tirada; `withRequiredArg` con `ArgTypes.STRING` recibe el texto y `context.get(roll)` lo entrega al núcleo.
- `setAllowsExtraArguments(true)` deja que la clase base reciba también las líneas con palabras sobrantes. El método `argumentsAfterCommand` detecta ese caso y responde con `USO`; así no se ejecuta una tirada parcial.
- `requireNoPermission()` evita exigir un permiso administrativo.
- `respond` captura `IllegalArgumentException` y envía solo el mensaje. Si aparece un error distinto, el servidor puede registrarlo; no prometas que ningún fallo inesperado dejará rastro.

**Comprueba:** el núcleo sigue sin importar clases de Hytale. Solo el paquete `curso.dado.hytale` conoce la API del servidor.

## 4. Compila y prueba el núcleo

En una terminal desde la raíz de `dado`, con `out/` y `build/` ignoradas por Git. Empieza con una compilación limpia para no arrastrar clases viejas.

Linux o macOS:

```text
rm -rf out build
javac -encoding UTF-8 -d out src/curso/dado/Dice.java
javac -encoding UTF-8 -d build/test-classes -cp out src/curso/dado/DiceTest.java
java -cp "out:build/test-classes" curso.dado.DiceTest
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force out,build -ErrorAction SilentlyContinue
javac -encoding UTF-8 -d out src/curso/dado/Dice.java
javac -encoding UTF-8 -d build\test-classes -cp out src/curso/dado/DiceTest.java
java -cp "out;build\test-classes" curso.dado.DiceTest
```

Las pruebas se compilan en `build/test-classes`, no dentro de `out/`; así no terminan dentro del JAR.

**Comprueba:** aparece `Pruebas del núcleo: OK`. Si aparece `AssertionError`, lee la etiqueta y corrige el caso; no cambies la prueba para ocultarlo.

## 5. Compila el adaptador contra el servidor

Indica la ruta de tu JAR oficial del servidor 0.7.7. No copies ese JAR al repositorio.

Linux o macOS:

```text
export HYTALE_SERVER_JAR="/ruta/a/Server-0.7.7.jar"
javac -encoding UTF-8 -d out -cp "out:$HYTALE_SERVER_JAR" \
  src/curso/dado/hytale/DadoPlugin.java \
  src/curso/dado/hytale/DadoCommand.java
```

Windows PowerShell:

```powershell
$env:HYTALE_SERVER_JAR = "C:\ruta\a\Server-0.7.7.jar"
javac -encoding UTF-8 -d out -cp "out;$env:HYTALE_SERVER_JAR" `
  src/curso/dado/hytale/DadoPlugin.java `
  src/curso/dado/hytale/DadoCommand.java
```

**Comprueba:** `javac` termina sin errores y `out/curso/dado/hytale/` contiene `DadoPlugin.class` y `DadoCommand.class`. Si dice que no encuentra `com.hypixel.hytale...`, la ruta del JAR o el separador del classpath están mal. No inventes clases de relleno para ocultar el error.

Esta compilación demuestra que las firmas usadas existen en la API 0.7.7; **no** demuestra que el plugin cargue ni que el comando responda.

## 6. Empaqueta el JAR

El servidor busca `manifest.json` en la raíz del JAR y las clases en la ruta de su paquete. Copia el manifiesto a `out/` y empaqueta esa carpeta completa.

Linux o macOS:

```text
cp manifest.json out/manifest.json
mkdir -p build
jar --create --file build/Dado-0.1.0.jar -C out .
```

Windows PowerShell:

```powershell
Copy-Item manifest.json out\manifest.json
New-Item -ItemType Directory -Force build | Out-Null
jar --create --file build\Dado-0.1.0.jar -C out .
```

Revisa el contenido:

```text
jar --list --file build/Dado-0.1.0.jar
```

Debe incluir, como mínimo:

```text
META-INF/MANIFEST.MF
curso/dado/Dice.class
curso/dado/hytale/DadoCommand.class
curso/dado/hytale/DadoCommand$WithRoll.class
curso/dado/hytale/DadoPlugin.class
manifest.json
```

**Comprueba:** `manifest.json` está en la raíz, no dentro de `META-INF` ni de otra carpeta. Si aparece `DiceTest.class` o una carpeta `test/`, empaquetaste las pruebas: corrige la ruta y vuelve a armar el JAR.

El manifiesto del ejemplo declara:

```json
{
  "Group": "EngiMods",
  "Name": "Dado",
  "Version": "0.1.0",
  "Description": "Ejemplo didáctico: tira dados desde el chat.",
  "Authors": [{"Name": "EngiMods"}],
  "Main": "curso.dado.hytale.DadoPlugin",
  "ServerVersion": "=0.7.7",
  "IncludesAssetPack": false
}
```

`Main` debe coincidir exactamente con la clase que extiende `JavaPlugin`. `ServerVersion` usa `=0.7.7` para exigir esa versión exacta; `0.7.7` sin `=` no es un rango válido. Ese detalle se comprobó con las clases oficiales 0.7.7 y debe conservarse al cambiar de versión. Si tu servidor es otra versión, cambia el valor por la versión exacta que uses, vuelve a compilar y no declares compatibilidad sin probarla.

## 7. Prepara la instalación local

1. Copia `build/Dado-0.1.0.jar` a la carpeta `mods/` de tu copia aislada del servidor. **No** copies el JAR, el servidor, `Assets.zip`, el mundo ni las configuraciones al repositorio.
2. Confirma primero la dirección de escucha y la autenticación oficial siguiendo L4. No abras puertos, no reenvíes puertos del router ni desactives la autenticación.
3. Arranca el servidor solo cuando tengas confirmado que escucha en loopback.
4. Conecta desde el mismo equipo, con tu cuenta legítima.

**Comprueba:** «el servidor arrancó», «el plugin cargó» y «`/dado` respondió» son tres hechos distintos. Registra cada uno por separado; una línea de arranque no prueba que el plugin se haya cargado.

## 8. Ejecuta la tabla de prueba

| Entrada | Resultado esperado | ¿Observado en el juego? |
|---|---|---|
| `/dado` | Un valor de 1 a 6 y su total. | Pendiente. |
| `/dado 2d6` | Dos valores de 1 a 6 y su suma, por ejemplo `2d6: [3, 5] = 8`. | Pendiente. |
| `/dado d20` | Un valor de 1 a 20. | Pendiente. |
| `/dado 0d6` | Mensaje que pide entre 1 y 20 dados. | Pendiente. |
| `/dado 2d1` | Mensaje que pide entre 2 y 100 caras. | Pendiente. |
| `/dado hola` | Mensaje que propone `2d6`. | Pendiente. |
| `/dado 2d6 extra` | Instrucción de uso; no se ejecuta una tirada parcial. | Pendiente. |

Anota también:

- versión exacta del servidor y del cliente;
- si el mensaje de error llegó como texto, sin un stacktrace visible para el jugador;
- si el comando apareció para una cuenta sin permisos de administrador;
- cualquier diferencia entre el mensaje del adaptador y el del analizador del servidor.

No marques una fila como observada sin haberla visto en el chat.

## Si algo falla

Orientaciones preventivas, no incidencias observadas en un servidor:

- **`package com.hypixel.hytale... does not exist`**: revisa `HYTALE_SERVER_JAR`, la ruta y el separador (`:` en Linux/macOS, `;` en Windows). No agregues stubs.
- **El JAR no contiene `manifest.json`**: copiaste el manifiesto a otra carpeta o empaquetaste `build/` en lugar de `out/`.
- **Hytale no encuentra la clase `Main`**: compara mayúsculas, paquete y nombre con `manifest.json`.
- **Error de `ServerVersion`**: usa `=0.7.7` para coincidencia exacta y valida el JSON.
- **`AssertionError` en el núcleo**: lee la etiqueta; el problema está en la lógica, no en el comando.
- **El comando no aparece en el juego**: no adivines. Detén la prueba, conserva la versión y el error depurado sin datos privados, y consulta la documentación de esa versión.
- **Argumentos sobrantes**: la clase base responde con `USO`. Si el servidor rechaza la línea antes, registra el mensaje real y ajusta la lección; no declares que tu guardia se ejecutó.

## Cómo lo haría un equipo

El adaptador aísla las llamadas de la API en un solo paquete. La compilación contra una versión exacta y el contenido del JAR se revisan antes de tocar el servidor. La prueba en juego se registra aparte, con fecha, versiones y resultado real. Una compilación correcta no sustituye esa prueba.

## Guarda tu avance

Revisa `git status`: deben aparecer las fuentes, `manifest.json` y la documentación; no `out/` ni `build/`. Luego:

```text
git add src/curso/dado/hytale/DadoPlugin.java src/curso/dado/hytale/DadoCommand.java
git commit -m "Conecta el comando con el núcleo"
```

**Comprueba:** `git log --oneline` incluye el commit y el JAR no quedó versionado. La prueba en juego se documenta en L7 cuando la completes.
