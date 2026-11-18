---
modulo: 3
orden: 1
titulo: Documenta y entrega
minutos: 30
estado: borrador; adaptador listo, prueba en juego pendiente
---

<!-- Contenido de la lección: copia desde aquí -->

Una entrega útil permite que otra persona repita tus pasos sin adivinar. En esta lección preparas documentación y una etiqueta, pero no envíes el ejercicio como plugin completo hasta que la integración y la prueba en juego estén resueltas.

## Al terminar podrás

- Documentar instrucciones, versiones y límites sin inventar resultados.
- Preparar una etiqueta Git para una entrega revisable.
- Reconocer cuándo un proyecto aún no cumple el ejercicio.

## Necesitas

El núcleo y pruebas de L5. El adaptador y el JAR de L6 ya existen y compilan; para la entrega completa necesitas además la prueba en un servidor aislado y todas las filas de L6 observadas en el juego.

## 1. Escribe un README honesto

En la raíz de `dado`, crea o amplía `README.md` con estos apartados:

```text
# Dado
Qué hace: comando /dado; límites y ejemplos.
Estado: núcleo, adaptador y JAR compilados; carga y respuesta en juego pendientes.
Requisitos: sistema, JDK, juego y API, con versiones exactas cuando se prueben.
Pruebas: comandos javac y java de la lección 5 y resultado observado.
Instalación y ejecución: pendiente de validar en servidor local.
Prueba manual: tabla de lección 6 y resultado real de cada caso.
Licencia: pendiente de elegir para código propio.
```

**Comprueba:** «Probado con» solo incluye combinaciones que tú ejecutaste, con fecha; una versión en un sitio web o un test del núcleo no es una prueba del juego. No incluyas secretos, mundo, JAR ni recursos del servidor.

## 2. Prepara licencia y repositorio

Elige una licencia para tu código propio y verifica la licencia de cualquier plantilla o dependencia antes de incorporarla. Puedes leer [Choose a License](https://choosealicense.com/) para conocer opciones; no afirmes tener permisos sobre archivos del juego. Crea un repositorio público vacío en un servicio admitido y sigue sus instrucciones de autenticación. No pegues tokens en la URL ni en archivos.

Cuando estés listo para compartir **el núcleo**, revisa `git status` y los archivos que subirás. Agrega el remoto con su URL pública, luego sube tu rama. **Comprueba:** solo aparecen fuentes y documentación. No es todavía una entrega final funcional.

## 3. Cuando la integración esté verificada

Repite las pruebas automáticas, compila el plugin con el procedimiento validado y ejecuta todos los casos de L6 localmente. Documenta comandos de instalación y retiro, las versiones exactas, fecha, resultado y pasos de reproducción. Corrige antes de continuar. **Comprueba:** el juego y el servidor realmente usados coinciden con lo declarado.

Guarda los cambios, y solo entonces crea y sube una etiqueta inmutable:

```text
git add README.md
git commit -m "Documenta la versión probada del plugin"
git tag -a v0.1.0 -m "Primera versión del plugin"
git push
git push origin v0.1.0
```

**Comprueba:** la etiqueta aparece en el repositorio público y apunta al commit revisado. Si corriges la entrega, usa otra etiqueta, por ejemplo `v0.1.1`, sin mover la anterior. Si existen otros archivos modificados, inclúyelos conscientemente en commits antes de etiquetar.

## 4. Envía cuando esté habilitado

En el ejercicio de esta lección, proporciona URL pública, versión real del juego, entorno y, en el comentario, etiqueta y una dificultad o decisión propia. Revisa los cinco criterios antes de enviar. **Comprueba:** la plataforma confirma el envío; si pide correcciones, crea un nuevo commit y etiqueta antes de reenviar.

## Si algo falla

Orientaciones preventivas: si Git dice que la etiqueta ya existe, revisa a qué apunta y usa una nueva para una corrección. Si el repositorio no es público, comprueba visibilidad antes de enviar. Si no tienes prueba en juego, conserva el estado pendiente: no rellenes versiones inventadas.

## Cómo lo haría un equipo

Una etiqueta fija permite revisar el mismo código; el README registra hechos observados, no promesas. Una integración sin probar es un bloqueo, no un aprobado parcial del plugin.

## Guarda tu avance

Guarda el README incluso si el juego está pendiente, con `git add README.md` y `git commit -m "Documenta el estado del proyecto"`. No crees la etiqueta de entrega completa hasta cumplir el paso 3.
