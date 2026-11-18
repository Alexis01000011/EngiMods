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
