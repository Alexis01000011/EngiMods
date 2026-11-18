---
modulo: 2
orden: 1
titulo: Crea tu proyecto
minutos: 30
estado: borrador
---

<!-- Contenido de la lección: copia desde aquí -->

Comenzarás con una carpeta pequeña y un historial Git. El ejemplo incluye un manifiesto y un procedimiento de compilación para armar tu primer JAR. La carga dentro del juego todavía está pendiente de comprobar.

## Al terminar podrás

- Crear una estructura para el núcleo y excluir datos privados.
- Guardar un primer commit y explicar qué falta para el plugin.

## Necesitas

Java y Git de la lección anterior. Para subir más adelante, crea un repositorio vacío en un servicio admitido por EngiMods.

## 1. Crea la carpeta de código

Dentro de `dado`, crea `src/curso/dado` desde tu explorador o editor. La ruta corresponde al paquete Java que escribirás en L5. **Comprueba:** puedes abrir la carpeta `src/curso/dado` en el editor.

Crea `.gitignore` en la raíz de `dado`:

```text
out/
build/
.gradle/
.idea/
*.class
*.jar
*.zip
Server/
mods/
universe/
logs/
.cache/
auth.enc
auth.key
config.json
permissions.json
```

Esta lista reduce riesgos, pero no garantiza detectar todos los secretos. **Comprueba:** no copiaste el servidor, recursos, mundos, tokens ni configuraciones del juego a `dado`.

## 2. Inicia Git

En una terminal abierta dentro de `dado`, ejecuta:

```text
git init
git status
git add .gitignore
git commit -m "Prepara el proyecto del dado"
```

**Comprueba:** `git status` muestra el árbol limpio. Si Git solicita identidad, configura nombre y correo apropiados para un repositorio público; el correo de un commit puede ser visible. No uses una cuenta de trabajo sin autorización.

## 3. Prepara el manifiesto

Guarda este archivo como `manifest.json` en la raíz del proyecto. Al empaquetar, quedará en la raíz del JAR. El campo `Main` dice qué clase carga Hytale; `Version` corresponde a tu plugin y `ServerVersion` a la referencia de servidor para la que se armó el ejemplo. El prefijo `=` de `ServerVersion` pide una coincidencia exacta: `0.7.7` sin `=` no es un rango válido.

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

**Comprueba:** el archivo se llama `manifest.json`, no `manifest.json.txt`. La clase indicada coincide con la que escribirás en L6. Guarda este cambio con `git add manifest.json` y `git commit -m "Agrega el manifiesto del plugin"`.

## Si algo falla

Son orientaciones preventivas: si `git` no se reconoce, abre una terminal nueva tras instalarlo. Si el commit falla por identidad, lee el error y configura una identidad adecuada. No publiques información privada para resolverlo.

## Cómo lo haría un equipo

Separa fuente de binarios y guarda cambios pequeños. El archivo ignorado no protege datos ya incluidos en un commit anterior; revisa siempre `git status` antes de agregar archivos.

## Guarda tu avance

Verifica el commit con `git log --oneline`. La siguiente lección explica la prueba del servidor y sus bloqueos; la lógica independiente está en L5.
