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
