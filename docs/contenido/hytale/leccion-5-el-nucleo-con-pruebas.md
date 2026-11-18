---
modulo: 2
orden: 3
titulo: El núcleo con pruebas
minutos: 45
estado: núcleo probado de forma aislada; lección sin prueba de alumno
---

<!-- Contenido de la lección: copia desde aquí -->

Aquí construyes el corazón del proyecto con Java puro. Las pruebas son un programa pequeño que falla si encuentra una respuesta incorrecta. No necesitan el juego ni una biblioteca externa; en un curso posterior puedes trasladarlas a JUnit.

## Al terminar podrás

- Leer y validar una notación como `2d6`.
- Generar dados y comprobar cantidad, límites y suma.
- Ejecutar pruebas reproducibles sin abrir Hytale.

## Necesitas

JDK 25 y el proyecto `dado` de L3. No necesitas completar la conexión de L4 para esta lección. Los comandos siguientes se ejecutan en una terminal desde la raíz de `dado`.

## 1. Escribe la lógica

Crea el archivo `src/curso/dado/Dice.java` y copia el bloque completo. `record` reúne cantidad y caras; el constructor valida también cuando se crea directamente. `parse` convierte texto y rechaza números demasiado grandes. `roll` recibe un generador para poder repetir los resultados en pruebas; `message` suma los valores.

```java
package curso.dado;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Reglas del dado: Java puro, sin dependencias del juego. */
public record Dice(int count, int sides) {
    private static final Pattern NOTATION = Pattern.compile("([0-9]*)d([0-9]+)");

    public Dice {
        if (count < 1 || count > 20) {
            throw new IllegalArgumentException("Usa entre 1 y 20 dados.");
        }
        if (sides < 2 || sides > 100) {
            throw new IllegalArgumentException("Usa dados de entre 2 y 100 caras.");
        }
    }

    public static Dice parse(String text) {
        if (text == null) {
            throw new IllegalArgumentException("Escribe una tirada como 2d6.");
        }
        Matcher match = NOTATION.matcher(text.trim().toLowerCase(Locale.ROOT));
        if (!match.matches()) {
            throw new IllegalArgumentException("Escribe una tirada como 2d6.");
        }
        try {
            int count = match.group(1).isEmpty() ? 1 : Integer.parseInt(match.group(1));
            return new Dice(count, Integer.parseInt(match.group(2)));
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Número demasiado grande; prueba 2d6.");
        }
    }

    public List<Integer> roll(Random random) {
        List<Integer> values = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            values.add(random.nextInt(sides) + 1);
        }
        return List.copyOf(values);
    }

    public String message(List<Integer> values) {
        int total = values.stream().mapToInt(Integer::intValue).sum();
        return count + "d" + sides + ": " + values + " = " + total;
    }
}
```

**Comprueba:** el nombre del archivo es `Dice.java`, el paquete es `curso.dado` y las llaves del código están completas. Los límites evitan cantidades desproporcionadas; `nextInt(sides) + 1` incluye tanto 1 como la última cara.

## 2. Escribe las pruebas

Crea `src/curso/dado/DiceTest.java`. La función `check` interrumpe el programa con `AssertionError` si algo es falso; no depende de activar las aserciones de Java. La semilla permite repetir la misma secuencia.

```java
package curso.dado;

import java.util.List;
import java.util.Random;

/** Pruebas ejecutables sin bibliotecas externas; falla con AssertionError. */
public class DiceTest {
    private static void check(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
    }

    private static void invalid(String input) {
        try {
            Dice.parse(input);
            throw new AssertionError("Aceptó: " + input);
        } catch (IllegalArgumentException expected) {
            check(!expected.getMessage().isBlank(), "Falta mensaje");
        }
    }

    public static void main(String[] args) {
        check(Dice.parse("2d6").equals(new Dice(2, 6)), "2d6");
        check(Dice.parse(" D20 ").equals(new Dice(1, 20)), "d20");
        check(Dice.parse("20d100").equals(new Dice(20, 100)), "máximos");
        check(Dice.parse("1d2").equals(new Dice(1, 2)), "mínimos");
        for (String bad : new String[]{"", "hola", "2d", "2d6+1", "0d6", "21d6", "2d1", "2d101", "99999999999d6", null}) invalid(bad);
        Dice dice = new Dice(20, 6);
        List<Integer> values = dice.roll(new Random(42));
        check(values.size() == 20, "cantidad");
        check(values.stream().allMatch(v -> v >= 1 && v <= 6), "rango");
        check(values.equals(dice.roll(new Random(42))), "semilla");
        check(new Dice(2, 6).message(List.of(3, 5)).equals("2d6: [3, 5] = 8"), "mensaje");
        Random random = new Random(1);
        boolean[] seen = new boolean[7];
        for (int i = 0; i < 100; i++) for (int value : dice.roll(random)) seen[value] = true;
        for (int i = 1; i <= 6; i++) check(seen[i], "cara " + i);
        System.out.println("Pruebas del núcleo: OK");
    }
}
```

**Comprueba:** los dos archivos tienen el mismo paquete. Las pruebas incluyen extremos, notación inválida, número enorme, azar reproducible, suma y que todas las caras aparecen en la secuencia fija. Ver que aparecen no demuestra estadísticamente que la distribución sea justa.

## 3. Compila y ejecuta

En Windows PowerShell, macOS o Linux:

```text
javac -d out src/curso/dado/Dice.java src/curso/dado/DiceTest.java
java -cp out curso.dado.DiceTest
```

**Comprueba:** aparece `Pruebas del núcleo: OK`. Si aparece `AssertionError`, lee la etiqueta y corrige el caso. `out/` contiene archivos generados y está ignorada por Git; no la publiques. Estas pruebas no significan que el plugin cargue.

## 4. Experimenta y restaura

Cambia temporalmente `random.nextInt(sides) + 1` por `random.nextInt(sides - 1) + 1`. Compila y ejecuta de nuevo. **Comprueba:** la prueba de la cara 6 falla. Restaura la expresión original y repite ambos comandos: vuelve a aparecer `Pruebas del núcleo: OK`. Así observas que el segundo límite de `nextInt` es exclusivo.

## Si algo falla

Orientaciones preventivas: si `javac` no se reconoce, vuelve a L2; si dice archivo no encontrado, verifica carpeta actual y mayúsculas de las rutas; si `Could not find or load main class`, revisa `-cp out` y el paquete. No cambies una prueba para ocultar un fallo: lee primero su etiqueta.

## Cómo lo haría un equipo

El núcleo no importa clases del juego. La entrada de azar se inyecta para obtener pruebas repetibles, y se revisan los bordes además del caso feliz. Una prueba automática no sustituye la prueba de integración en servidor.

## Guarda tu avance

Revisa `git status`; deben verse las fuentes, no `out/`. Luego:

```text
git add src/curso/dado/Dice.java src/curso/dado/DiceTest.java
git commit -m "Implementa y prueba el núcleo del dado"
```

**Comprueba:** `git log --oneline` incluye el commit. En L6 diseñarás la conexión sin asumir que ya funciona.
