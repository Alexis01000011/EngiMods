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
