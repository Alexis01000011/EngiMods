---
modulo: 2
orden: 2
titulo: Ejecuta el servidor local
minutos: 20
estado: arranque y conexión local pendientes de prueba real
---

<!-- Contenido de la lección: copia desde aquí -->

Esta lección prepara el servidor para probar el plugin. El adaptador y el JAR se construyen en L6; si todavía no los tienes, puedes completar L5 y L6 primero y volver aquí para la prueba en juego. El objetivo es ejecutar un servidor **solo en tu equipo**, con autenticación oficial, sin exponerlo a internet. El arranque y la conexión del cliente todavía no se han verificado en este borrador: trátalos como un procedimiento a confirmar, no como una receta probada.

## Al terminar podrás

- Separar los archivos del servidor, el JAR del plugin y el repositorio.
- Reconocer por qué `0.0.0.0` no sirve para un laboratorio local.
- Distinguir «el servidor arrancó» de «el plugin cargó» y de «el comando respondió».

## Necesitas

- La instalación legítima del juego y Java 25.
- Una copia de `Server` y `Assets.zip` obtenida según **Server Files** del [manual oficial](https://support.hytale.com/hc/en-us/articles/45326769420827-Hytale-Server-Manual).
- El JAR `Dado-0.1.0.jar` de L6. Si aún no lo armaste, vuelve a esta lección después de L6.
- Una cuenta legítima. No uses cuentas compartidas ni servidores de otras personas.

## 1. Prepara una copia aislada

1. Crea una carpeta de laboratorio fuera de `dado` y fuera de cualquier repositorio. Por ejemplo, `hytale-lab`.
2. Copia ahí `Server` y `Assets.zip` desde tu instalación legítima.
3. Copia `Dado-0.1.0.jar` a la carpeta `mods/` de esa copia aislada. Si `mods/` no existe, créala.
4. No copies el servidor, los recursos, el mundo, `auth.enc`, `auth.key`, `config.json` ni `permissions.json` al repositorio.

**Comprueba:** el repositorio solo contiene fuentes, manifiesto y documentación. El servidor y el JAR viven en `hytale-lab`.

## 2. Revisa red y autenticación antes de arrancar

El manual indica que el valor predeterminado documentado escucha en `0.0.0.0:5520`. Esa dirección acepta conexiones en todas las interfaces; **no la uses para este curso**.

Para el laboratorio necesitas una dirección de loopback. El manual documenta la opción `--bind`, pero la sintaxis exacta para loopback y la conexión del cliente no se han comprobado en este borrador. Antes de ejecutar:

- lee la sección de `--bind` del manual de tu versión;
- confirma cómo se escribe una dirección local en tu sistema;
- no adivines ni cambies la configuración de red para que «funcione».

Un candidato a verificar, **no una orden probada**, tiene esta forma:

```text
<comando-de-arranque-del-manual> --bind 127.0.0.1:5520
```

Si tu copia del manual usa otra sintaxis, esa manda. Detente si no puedes confirmar que el servidor escuchará solo en loopback.

Nunca para esta práctica:

- abras puertos en el router o en el cortafuegos;
- reenvíes puertos;
- uses `0.0.0.0` «para que conecte»;
- desactives la autenticación o cualquier control de seguridad;
- compartas códigos de dispositivo, tokens o archivos de autenticación.

Con el servidor detenido, aún no hay nada que comprobar. Cuando lo arranques, revisa desde el sistema operativo que el puerto solo aparece en una dirección local. Son comprobaciones del sistema, no del juego:

Linux:

```text
ss -ltn | grep 5520
```

macOS:

```text
lsof -nP -iTCP:5520 -sTCP:LISTEN
```

Windows PowerShell:

```powershell
Get-NetTCPConnection -LocalPort 5520 | Select-Object LocalAddress,State
```

**Comprueba:** la dirección local es `127.0.0.1` o `::1`, no `0.0.0.0` ni `::`. Si aparece una dirección abierta, apaga el servidor y corrige el arranque antes de continuar.

## 3. Arranca y busca evidencia

1. Abre una terminal dentro de `hytale-lab`, no dentro de `dado`.
2. Ejecuta el comando de arranque del manual con la opción de loopback que hayas confirmado.
3. Anota la versión exacta del servidor y la hora.
4. Busca en la salida evidencia de que el plugin se cargó. No existe una línea universal que puedas copiar de este borrador: registra el texto real que veas.

**Comprueba:** no declares éxito solo porque apareció «servidor iniciado». Un plugin puede faltar, fallar al cargar o no registrar el comando. La carga del plugin es un hecho separado.

## 4. Conecta desde el mismo equipo

1. Abre el cliente en el mismo equipo. La versión exacta del cliente se confirma en este paso y se registra; no la inventes.
2. Usa la autenticación oficial que solicite el juego o el servidor. Mantén privado cualquier código de dispositivo o token.
3. Conéctate solo a la dirección local. No invites a otras personas ni pruebes desde otra computadora.
4. Ejecuta la tabla de L6 y registra cada resultado.

**Comprueba:** si el cliente no conecta, no abras puertos ni desactives autenticación. Detén la prueba, guarda el mensaje de error sin datos privados y revisa la dirección de escucha y la versión.

## 5. Cierra de forma segura

1. Ejecuta el comando de apagado que documente tu servidor.
2. Espera a que el proceso termine y confirma que el puerto ya no está escuchando.
3. Guarda las notas de la prueba fuera del repositorio si contienen rutas o datos privados.

**Comprueba:** no queda un proceso del servidor en segundo plano.

## Registro mínimo

| Dato | Valor |
|---|---|
| Fecha y persona | |
| Sistema operativo y arquitectura | |
| Versión exacta del servidor y fuente | |
| Versión exacta del cliente y canal | |
| Java/JDK y compilador | |
| JAR del plugin y su hash | |
| Dirección de escucha observada | |
| Evidencia de carga del plugin | |
| Resultado de cada fila de L6 | |
| Error depurado, sin datos privados | |

## Si algo falla

Son orientaciones preventivas; los fallos reales se añadirán cuando alguien complete la prueba:

- **El servidor rechaza `--bind`**: no cambies a `0.0.0.0`. Revisa la sintaxis del manual de tu versión y detente si no puedes confirmar loopback.
- **El puerto aparece abierto**: apaga el servidor, corrige el arranque y no conectes hasta aislarlo.
- **La autenticación pide un código**: mantenlo privado y sigue el flujo oficial. No desactives la autenticación para evitarlo.
- **El cliente no conecta**: registra versión y mensaje; comprueba que usas la misma máquina y la dirección local. No abras puertos.
- **El plugin no aparece**: revisa que el JAR esté en `mods/`, que `manifest.json` esté en la raíz del JAR y que `Main` coincida con la clase. No declares que el comando existe.
- **El comando aparece pero falla**: conserva el mensaje exacto y la versión; no compartas tokens ni rutas privadas.

## Cómo lo haría un equipo

Una prueba segura delimita red, datos y entorno antes de ejecutar. El registro separa arranque, carga del plugin y respuesta del comando; así se diagnostica sin compartir credenciales ni mundos.

## Guarda tu avance

Anota en tu README de trabajo el estado real. Si todavía no probaste, escribe:

```text
Servidor local y plugin: arranque y conexión pendientes de verificación.
```

Guarda la nota:

```text
git add README.md
git commit -m "Documenta el estado del servidor local"
```

**Comprueba:** el README no afirma una versión de cliente ni una prueba que no hiciste. Si aún no armaste el JAR, continúa con L5 y L6; vuelve a esta lección para la prueba en juego.
