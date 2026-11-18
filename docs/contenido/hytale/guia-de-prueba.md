# Guía de prueba para el equipo

Estado al 18/11/2026: el núcleo, el adaptador y el empaquetado se verificaron en una estación de trabajo con JDK 25.0.5.0.3 y el JAR oficial del servidor 0.7.7; no se arrancó el servidor ni se probó el juego. Las lecciones siguen sin prueba de alumno. No publicar la práctica completa ni registrar `LessonTest` hasta completar L4 y L6 de punta a punta y confirmar la versión del cliente. La muestra conceptual puede evaluarse por separado; su publicación requiere aprobación del equipo y revisión de marca.

## Antes de iniciar

- Elige una persona con juego legítimo y una computadora de prueba, preferentemente limpia; anota lo previamente instalado. No uses cuentas, bases ni servidores compartidos.
- El adaptador y el manifiesto ya existen en `ejemplo/`. No los reescribas desde cero: comprueba que el JAR se arma y luego valida la carga y la respuesta en el juego.
- Confirma con el manual oficial la sintaxis de `--bind` para loopback y cómo conectar el cliente desde el mismo equipo. **No abrir puertos, modificar el router o el cortafuegos, ni desactivar autenticación**; si no se logra probar el aislamiento, detener.
- Asegura una copia local aislada de archivos de servidor y recursos; no ponerla dentro del repositorio. Nunca recopiles códigos de dispositivo, tokens, llaves, registros sin depurar o datos privados.
- Comprueba marca, EULA, Creator Policy y condiciones comerciales vigentes con las fuentes oficiales y el equipo. Resolver precio, acceso, aviso, responsable de prueba y repositorio plantilla antes de publicar.

## Verificación de compilación y empaquetado

Estos pasos ya se ejecutaron en la estación de referencia (Linux/POSIX). Repítelos desde un clon limpio y registra diferencias. En Windows PowerShell usa los comandos de L6, con separadores `;` y `Copy-Item`/`New-Item`. No copies el JAR oficial del servidor al repositorio.

```text
# Desde docs/contenido/hytale/ejemplo o una copia de trabajo
rm -rf out build
javac -encoding UTF-8 -d out src/curso/dado/Dice.java
javac -encoding UTF-8 -d build/test-classes -cp out src/curso/dado/DiceTest.java
java -cp "out:build/test-classes" curso.dado.DiceTest
javac -encoding UTF-8 -d out -cp "out:/ruta/a/Server-0.7.7.jar" \
  src/curso/dado/hytale/DadoPlugin.java \
  src/curso/dado/hytale/DadoCommand.java
cp manifest.json out/manifest.json
mkdir -p build
jar --create --file build/Dado-0.1.0.jar -C out .
jar --list --file build/Dado-0.1.0.jar
```

Comprueba:

- salida `Pruebas del núcleo: OK`;
- `Dado-0.1.0.jar` contiene `manifest.json` en la raíz y las clases `Dice`, `DadoPlugin`, `DadoCommand` y `DadoCommand$WithRoll`;
- no contiene `DiceTest.class` ni archivos del servidor;
- `PluginManifest.CODEC` decodifica el manifiesto con `ServerVersion =0.7.7`; el rango acepta la versión `0.7.7` y rechaza `0.7.8`;
- cargar la clase `Main` con un `URLClassLoader` confirma que extiende `JavaPlugin` y tiene el constructor `JavaPluginInit`.

Una compilación correcta no autoriza a decir que el plugin carga. El registro de esa prueba va aparte.

## Registro de evidencia

| Campo | Registrar |
|---|---|
| Fecha y persona que ejecuta | |
| Sistema operativo, arquitectura, RAM y espacio libre | |
| Versión exacta del cliente y canal | |
| Versión exacta del servidor y fuente | |
| API/dependencia y versión, fuente y fecha | |
| Java/JDK y compilador completos | |
| Herramienta de compilación, versión y plantilla/licencia | |
| Repositorio, commit o etiqueta probada | |
| JAR propio: nombre, tamaño y hash SHA-256 | |
| Dirección de escucha y evidencia de aislamiento sin datos sensibles | |
| Evidencia de carga del plugin | |
| Por lección: duración, pasos, resultado, discrepancia y error depurado | |
| Revisor independiente, fecha y hallazgos | |

No confundir `release 0.7.7` visto en documentación y metadatos con versión instalada o prueba de compatibilidad. Documentar la fuente de cada dato. Una prueba del núcleo o una compilación no autoriza un sello de juego.

## Casos por lección

1. **Muestra:** pedir a una persona que explique `2d6`, `0d6`, núcleo, adaptador y «Probado con»; registrar confusiones y tiempo. Contrastar el ejemplo de salida con la implementación definitiva.
2. **Laboratorio:** verificar instalación y comandos en el sistema elegido, versión real de Java/Git, rutas del launcher y requisitos de memoria y espacio. Registrar capturas solo sin datos sensibles.
3. **Proyecto:** comprobar estructura, exclusiones, primer commit, manifiesto, `Main`, `Version`, `ServerVersion =0.7.7`, coordenadas y construcción reproducible desde un clon limpio. Verificar que ningún artefacto del juego entre al repositorio. El manifiesto debe decodificarse con las clases oficiales; `0.7.7` sin `=` no es un rango válido.
4. **Servidor:** comprobar dirección exclusivamente local con evidencia apropiada, autenticación oficial, arranque, carga del plugin, conexión en la misma máquina y cierre seguro. Registrar la versión real del cliente. Detener si no hay aislamiento confirmado.
5. **Núcleo:** copiar literalmente los dos bloques, ejecutar ambos comandos, verificar salida y fallo inducido, restaurar y repetir; comparar las fuentes con el ejemplo de esta carpeta. Registrar tiempo y diferencias entre sistemas.
6. **Integración:** compilar contra el JAR 0.7.7 exacto; verificar registro, argumento ausente, argumento válido e inválido, argumentos extra, respuesta al emisor, ausencia de stacktrace visible, permisos y cada fila de la tabla en juego. Registrar cualquier cambio de firma y causa. No dar por hecho que la guardia de argumentos extra se ejecutó si el servidor rechazó la línea antes.
7. **Entrega:** comprobar que el README y la licencia se pueden seguir desde un clon limpio, que la etiqueta apunta al commit final y que no hay secretos ni binarios. Cuando exista un entorno autorizado, el equipo revisará por separado el flujo de envío y revisión de la plataforma; no usar una base compartida sin autorización.

## Qué está verificado y qué falta

Verificado en la estación de referencia:

- el núcleo compila y pasa `Pruebas del núcleo: OK`;
- el adaptador compila contra el JAR oficial 0.7.7;
- el JAR propio contiene el manifiesto en la raíz y las clases esperadas;
- el manifiesto se decodifica y `ServerVersion` es exacto;
- la clase `Main` extiende `JavaPlugin` y tiene el constructor esperado.

No verificado:

- arranque del servidor con la copia aislada;
- dirección de loopback y ausencia de exposición;
- autenticación oficial de punta a punta;
- versión exacta del cliente;
- carga real del plugin;
- registro de `/dado` y respuesta en el chat;
- las siete filas de L6, incluida la de argumentos extra;
- que un error de entrada no muestre stacktrace en el cliente;
- comportamiento con una cuenta sin permisos administrativos.

## Cierre y «Probado con»

1. Corregir cada paso ambiguo y reemplazar orientaciones preventivas por incidencias efectivamente observadas; ajustar tiempos y resolver todos los `[VERIFICAR]`.
2. Otra persona revisa voz, exactitud, marca, seguridad, licencias, enlaces, código y coherencia con modelos. No copiar archivos de juego al repositorio.
3. Por cada lección, solo si se siguió completa y exitosamente en el juego y entorno declarados, capturar `LessonTest` con `GameVersion`, `ModdingEnvironment` del mismo juego y fecha real. Para una lección conceptual sin ejecución en juego, mantener «Sin versión probada» salvo que se haya hecho también esa prueba real; no inventar un sello.
4. Capturar primero en borrador, con precio y acceso decididos por el equipo. La muestra se marca `is_sample` solo con aprobación. Publicar la práctica completa únicamente tras resolver bloqueos, revisión y pruebas reales.
