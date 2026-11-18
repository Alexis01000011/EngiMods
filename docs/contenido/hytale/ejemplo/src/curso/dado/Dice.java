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
