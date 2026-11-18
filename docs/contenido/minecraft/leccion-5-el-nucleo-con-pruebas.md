---
curso: Misión Cero: tu primer mod para Minecraft
modulo: "2. Tu primer mod"
orden: 3
titulo: "El núcleo: la lógica del dado con pruebas"
minutos: 45
estado: borrador sin probar
---

<!-- Contenido de la lección: copia desde aquí -->

Esta es la lección más importante de la Misión Cero. Vas a escribir la lógica del dado en Java puro, sin nada de Minecraft, y la vas a comprobar con pruebas automáticas que corren en segundos. Así sabes que tu lógica funciona antes de abrir el juego, y lo sigues sabiendo cuando Minecraft cambie de versión.

## Al terminar podrás

- Agregar JUnit a tu proyecto y correr pruebas con Gradle.
- Escribir una prueba antes del código y verla pasar de rojo a verde.
- Validar lo que escribe el jugador con mensajes que dicen qué hacer.
- Explicar por qué una prueba en verde no garantiza que el código esté bien.

## Necesitas

- La lección **Ejecuta el juego con tu mod** completa.
- Saber qué es una clase y un método. Si nunca has escrito Java, no te preocupes: cada bloque trae su explicación.

## Por qué un núcleo aparte

Para probar algo dentro de Minecraft tienes que arrancar el juego, entrar a un mundo y escribir el comando a mano. Toma un minuto cada vez, y es fácil olvidar un caso.

Si la lógica no depende de Minecraft, una prueba la revisa en milisegundos, siempre de la misma forma. Por eso tu núcleo vive en su propio paquete, `core`, y tiene una regla: **nada en `core` importa algo de `net.minecraft` ni de `net.fabricmc`.**

## 1. Agrega JUnit

JUnit es la biblioteca de pruebas más usada en Java. Abre `build.gradle` y busca el bloque `dependencies { ... }`. Agrega estas tres líneas **dentro** del bloque, debajo de las que ya tiene:

```groovy
testImplementation platform("org.junit:junit-bom:6.1.3")
testImplementation "org.junit.jupiter:junit-jupiter"
testRuntimeOnly "org.junit.platform:junit-platform-launcher"
```

Al final del archivo, fuera de cualquier otro bloque, agrega:

```groovy
test {
    useJUnitPlatform()
}
```

`[VERIFICAR: que la plantilla de 26.3 use build.gradle en Groovy y no traiga ya un bloque test]`

Sincroniza Gradle con el botón de recargar del panel **Gradle**.

**Comprueba:** la sincronización termina sin errores.

## 2. Escribe tu primera prueba

Vas a escribir la prueba **antes** que el código. Primero dices qué esperas; luego haces que pase.

Crea la carpeta de pruebas y el paquete: en el panel del proyecto, clic derecho en `src` › **New › Directory** › `test/java`. Dentro, crea el paquete `io.github.tuusuario.dado.core` (con tu usuario, igual que en tu código).

En `src/test/java/io/github/tuusuario/dado/core/DiceRollTest.java`:

```java
package io.github.tuusuario.dado.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class DiceRollTest {

    @Test
    void readsCountAndSides() {
        assertEquals(new DiceRoll(2, 6), DiceRoll.parse("2d6"));
    }
}
```

La prueba dice: "si leo el texto `2d6`, obtengo una tirada de 2 dados de 6 caras". Algunos `import` todavía no se usan; IntelliJ IDEA los muestra en gris. Los vas a usar en un momento.

> ※ Escribimos el código en inglés porque es lo que vas a ver en cualquier equipo y en la documentación de Fabric. Los mensajes que ve el jugador van en español.

Corre las pruebas:

- Windows (PowerShell): `.\gradlew test`
- macOS, Linux o Git Bash: `./gradlew test`

**Comprueba:** falla con un error como `cannot find symbol: class DiceRoll`. Es lo esperado: la prueba pide algo que todavía no existe. Eso es el **rojo**.

## 3. Escribe el código que la hace pasar

Crea el paquete `io.github.tuusuario.dado.core` dentro de `src/main/java` (clic derecho en el paquete de tu mod › **New › Package** › `core`).

En `src/main/java/io/github/tuusuario/dado/core/DiceRoll.java`:

```java
package io.github.tuusuario.dado.core;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Una tirada como "2d6": cuántos dados se tiran y cuántas caras tiene cada uno. */
public record DiceRoll(int count, int sides) {

    public static final int MAX_COUNT = 20;
    public static final int MAX_SIDES = 100;

    private static final Pattern NOTATION = Pattern.compile("(\\d*)d(\\d+)");

    public DiceRoll {
        if (count < 1 || count > MAX_COUNT) {
            throw new IllegalArgumentException(
                    "Puedes tirar de 1 a " + MAX_COUNT + " dados a la vez.");
        }
        if (sides < 2 || sides > MAX_SIDES) {
            throw new IllegalArgumentException(
                    "Un dado puede tener de 2 a " + MAX_SIDES + " caras.");
        }
    }

    /** Lee textos como "2d6", "d20" o "1D8". Si el texto no sirve, lanza IllegalArgumentException. */
    public static DiceRoll parse(String text) {
        Matcher matcher = NOTATION.matcher(text.trim().toLowerCase());
        if (!matcher.matches()) {
            throw new IllegalArgumentException(
                    "Escribe la tirada como 2d6: cuántos dados, una d y cuántas caras.");
        }
        try {
            String count = matcher.group(1);
            return new DiceRoll(
                    count.isEmpty() ? 1 : Integer.parseInt(count),
                    Integer.parseInt(matcher.group(2)));
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException(
                    "Ese número es demasiado grande. Prueba con algo como 2d6.");
        }
    }

    @Override
    public String toString() {
        return count + "d" + sides;
    }
}
```

Qué hace cada parte:

- **`record`** es una clase para datos que no cambian. Java le crea solo el constructor, `count()`, `sides()` y la comparación con `equals`, que es lo que usa `assertEquals` en tu prueba.
- **El constructor compacto** (`public DiceRoll { ... }`) revisa los límites. Así no puede existir una tirada imposible, como `0d6`, se cree como se cree.
- **Los límites** (20 dados y 100 caras) evitan que alguien escriba `1000d1000` y llene el chat. Son constantes con nombre para que se lean y se cambien en un solo lugar.
- **`NOTATION`** es una expresión regular: "cero o más dígitos, una `d`, uno o más dígitos". Si no hay número antes de la `d`, se tira un dado.
- **Los mensajes de error** dicen qué hacer, no solo que algo está mal. El jugador los va a ver en el chat.

Corre `./gradlew test` (o `.\gradlew test`) otra vez.

**Comprueba:** dice `BUILD SUCCESSFUL`. Es el **verde**.

Guarda este paso:

```text
git add .
git commit -m "Lee tiradas como 2d6 con su primera prueba"
```

## 4. Prueba los casos difíciles

Una sola prueba cubre el caso feliz. Los errores suelen estar en lo que nadie espera. Agrega estas pruebas dentro de `DiceRollTest`, debajo de la primera:

```java
    @Test
    void withoutCountRollsOneDie() {
        assertEquals(new DiceRoll(1, 20), DiceRoll.parse("d20"));
    }

    @Test
    void ignoresCaseAndSpaces() {
        assertEquals(new DiceRoll(3, 8), DiceRoll.parse(" 3D8 "));
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "dado", "2d", "2x6", "-1d6", "2d6+1", "99999999999d6"})
    void rejectsTextThatIsNotARoll(String text) {
        assertThrows(IllegalArgumentException.class, () -> DiceRoll.parse(text));
    }

    @ParameterizedTest
    @ValueSource(strings = {"0d6", "21d6", "2d1", "2d101"})
    void rejectsRollsOutOfRange(String text) {
        assertThrows(IllegalArgumentException.class, () -> DiceRoll.parse(text));
    }
```

`@ParameterizedTest` corre la misma prueba con cada texto de la lista. Así pruebas once entradas malas sin escribir once pruebas.

Corre las pruebas. Para ver el detalle, abre en tu navegador `build/reports/tests/test/index.html`.

**Comprueba:** el reporte dice **14 tests, 0 failures**.

<details>
<summary>Reto: ¿por qué <code>99999999999d6</code> necesita su propio caso?</summary>
<p>El número cumple la expresión regular, pero no cabe en un <code>int</code>, y <code>Integer.parseInt</code> lanza <code>NumberFormatException</code>. Sin el <code>try</code> en <code>parse</code>, ese error llegaría al juego como un error raro en lugar de un mensaje claro. Quita el <code>try</code> un momento, corre las pruebas y mira cuál falla.</p>
</details>

## 5. Tira los dados

Ahora la tirada. El resultado necesita su propia clase: los valores que salieron, el total y el mensaje para el chat.

En `src/main/java/io/github/tuusuario/dado/core/RollResult.java`:

```java
package io.github.tuusuario.dado.core;

import java.util.List;
import java.util.stream.Collectors;

/** Lo que salió en una tirada. */
public record RollResult(DiceRoll roll, List<Integer> values) {

    public RollResult {
        values = List.copyOf(values);
    }

    public int total() {
        return values.stream().mapToInt(Integer::intValue).sum();
    }

    /** El mensaje que verá el jugador, por ejemplo "2d6: 3 + 5 = 8". */
    public String message() {
        if (values.size() == 1) {
            return roll + ": " + total();
        }
        String sum = values.stream().map(String::valueOf).collect(Collectors.joining(" + "));
        return roll + ": " + sum + " = " + total();
    }
}
```

Y en `DiceRoll.java` agrega este método, antes de `toString()`:

```java
    /** Tira los dados con el generador que le pases. */
    public RollResult roll(RandomGenerator random) {
        List<Integer> values = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            values.add(random.nextInt(1, sides + 1));
        }
        return new RollResult(this, values);
    }
```

Agrega también sus `import` arriba, junto a los otros:

```java
import java.util.ArrayList;
import java.util.List;
import java.util.random.RandomGenerator;
```

Dos decisiones de diseño:

- **`roll` recibe el generador de números al azar** en lugar de crearlo adentro. En el juego le pasas uno de verdad; en las pruebas, uno con **semilla** (`new Random(42)`), que siempre da los mismos números. Así una prueba con azar da siempre el mismo resultado.
- **`List.copyOf`** guarda una copia que nadie puede cambiar. Si alguien modifica la lista original, tu resultado sigue igual.

Ahora las pruebas. Agrégalas en `DiceRollTest`:

```java
    @Test
    void rollsOneValuePerDieWithinRange() {
        RollResult result = new DiceRoll(20, 6).roll(new Random(42));

        assertEquals(20, result.values().size());
        assertTrue(result.values().stream().allMatch(v -> v >= 1 && v <= 6));
    }

    @Test
    void sameSeedGivesSameResult() {
        DiceRoll roll = new DiceRoll(5, 20);

        assertEquals(roll.roll(new Random(7)), roll.roll(new Random(7)));
    }

    @Test
    void messageShowsEachDieAndTheTotal() {
        RollResult result = new RollResult(new DiceRoll(2, 6), List.of(3, 5));

        assertEquals(8, result.total());
        assertEquals("2d6: 3 + 5 = 8", result.message());
    }

    @Test
    void messageForOneDieShowsOnlyTheValue() {
        RollResult result = new RollResult(new DiceRoll(1, 20), List.of(17));

        assertEquals("1d20: 17", result.message());
    }
```

**Comprueba:** `./gradlew test` termina con `BUILD SUCCESSFUL` y el reporte dice **18 tests, 0 failures**.

```text
git add .
git commit -m "Tira los dados y arma el mensaje del resultado"
```

## 6. Rompe tu código a propósito

En `DiceRoll.roll`, cambia `sides + 1` por `sides`. Es un error muy común: en `nextInt(1, sides + 1)` el segundo número **no** se incluye, así que ahora tu dado de 6 caras nunca saca 6.

Corre las pruebas.

**Comprueba:** las 18 siguen en verde. Tus pruebas no ven este error.

Una prueba en verde solo dice que el código hace lo que la prueba revisa. `rollsOneValuePerDieWithinRange` revisa que cada valor esté entre 1 y 6, pero nunca que el 6 pueda salir. Agrega una prueba que sí lo revise:

```java
    @Test
    void everyFaceCanComeUp() {
        Random random = new Random(1);
        Set<Integer> seen = new HashSet<>();
        for (int i = 0; i < 50; i++) {
            seen.addAll(new DiceRoll(20, 6).roll(random).values());
        }

        assertEquals(Set.of(1, 2, 3, 4, 5, 6), seen);
    }
```

Tira 50 veces 20 dados (mil valores) y revisa que hayan salido las seis caras.

**Comprueba:** ahora falla **solo** `everyFaceCanComeUp`. En su mensaje, `expected` trae las seis caras y `but was` trae solo del 1 al 5.

Regresa `sides + 1` y corre las pruebas.

**Comprueba:** **19 tests, 0 failures**.

```text
git add .
git commit -m "Prueba que pueden salir todas las caras del dado"
```

<details>
<summary>Ver el archivo de pruebas completo</summary>
<p>En <code>src/test/java/io/github/tuusuario/dado/core/DiceRollTest.java</code>:</p>
<pre><code>package io.github.tuusuario.dado.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class DiceRollTest {

    @Test
    void readsCountAndSides() {
        assertEquals(new DiceRoll(2, 6), DiceRoll.parse("2d6"));
    }

    @Test
    void withoutCountRollsOneDie() {
        assertEquals(new DiceRoll(1, 20), DiceRoll.parse("d20"));
    }

    @Test
    void ignoresCaseAndSpaces() {
        assertEquals(new DiceRoll(3, 8), DiceRoll.parse(" 3D8 "));
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "dado", "2d", "2x6", "-1d6", "2d6+1", "99999999999d6"})
    void rejectsTextThatIsNotARoll(String text) {
        assertThrows(IllegalArgumentException.class, () -&gt; DiceRoll.parse(text));
    }

    @ParameterizedTest
    @ValueSource(strings = {"0d6", "21d6", "2d1", "2d101"})
    void rejectsRollsOutOfRange(String text) {
        assertThrows(IllegalArgumentException.class, () -&gt; DiceRoll.parse(text));
    }

    @Test
    void rollsOneValuePerDieWithinRange() {
        RollResult result = new DiceRoll(20, 6).roll(new Random(42));

        assertEquals(20, result.values().size());
        assertTrue(result.values().stream().allMatch(v -&gt; v &gt;= 1 &amp;&amp; v &lt;= 6));
    }

    @Test
    void everyFaceCanComeUp() {
        Random random = new Random(1);
        Set&lt;Integer&gt; seen = new HashSet&lt;&gt;();
        for (int i = 0; i &lt; 50; i++) {
            seen.addAll(new DiceRoll(20, 6).roll(random).values());
        }

        assertEquals(Set.of(1, 2, 3, 4, 5, 6), seen);
    }

    @Test
    void sameSeedGivesSameResult() {
        DiceRoll roll = new DiceRoll(5, 20);

        assertEquals(roll.roll(new Random(7)), roll.roll(new Random(7)));
    }

    @Test
    void messageShowsEachDieAndTheTotal() {
        RollResult result = new RollResult(new DiceRoll(2, 6), List.of(3, 5));

        assertEquals(8, result.total());
        assertEquals("2d6: 3 + 5 = 8", result.message());
    }

    @Test
    void messageForOneDieShowsOnlyTheValue() {
        RollResult result = new RollResult(new DiceRoll(1, 20), List.of(17));

        assertEquals("1d20: 17", result.message());
    }
}</code></pre>
</details>

## 7. Comprueba que el núcleo no conoce Minecraft

En IntelliJ IDEA, clic derecho en el paquete `core` (en `src/main/java`) › **Find in Files**. Busca `net.minecraft` y después `net.fabricmc`.

**Comprueba:** las dos búsquedas dicen **0 matches**. Si aparece algo, muévelo fuera de `core`: en la siguiente lección ves a dónde.

## Si algo falla

`[VERIFICAR: completar con los errores encontrados en la prueba real. Abajo, los más probables; quitar los que no aparezcan.]`

- **`./gradlew test` dice `NO-SOURCE` o no corre ninguna prueba:** la prueba no está en `src/test/java` o falta el bloque `test { useJUnitPlatform() }` en `build.gradle`.
- **`package org.junit.jupiter.api does not exist`:** las líneas de JUnit no quedaron dentro de `dependencies { ... }` o no sincronizaste Gradle después de agregarlas.
- **`cannot find symbol` en `RandomGenerator` o `ArrayList`:** faltan los `import` del paso 5. En IntelliJ IDEA, pon el cursor en la palabra en rojo y presiona <kbd>Alt</kbd> + <kbd>Enter</kbd> (<kbd>Option</kbd> + <kbd>Enter</kbd> en macOS) › **Import class**.
- **El paquete de la prueba no coincide con el del código:** los dos deben ser `io.github.tuusuario.dado.core`, con tu usuario.

## Cómo lo haría un equipo

- **Separar el núcleo del adaptador.** La lógica que importa no depende del juego. Se prueba rápido y sobrevive a las actualizaciones. Es la misma idea que vas a usar en mods más grandes.
- **Rojo, verde y luego mejorar.** Escribir la prueba primero te obliga a decidir qué quieres antes de cómo hacerlo.
- **Probar los bordes.** Los errores viven en los límites: cero, el máximo, un texto vacío, un número enorme.
- **Una prueba en verde no es una garantía.** Romper el código a propósito te dice si tus pruebas sirven.

## Guarda tu avance

Ya hiciste tres *commits* en esta lección. Súbelos:

```text
git push
```

**Comprueba:** en GitHub ves tus *commits* nuevos. En la siguiente lección, **Conecta el núcleo al juego**, el comando `/dado` usa esta lógica dentro de Minecraft.
