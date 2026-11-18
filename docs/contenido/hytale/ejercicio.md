---
leccion: Documenta y entrega
titulo: "Tu primer plugin: el comando /dado"
estado: adaptador y paquete disponibles; prueba en juego pendiente
---

# Ejercicio y rúbrica

Captura las instrucciones siguientes como `Exercise.instructions` de L7, solo después de resolver la prueba de integración en juego. `is_final_project=False`: no se exige publicar un mod en un marketplace.

## Instrucciones

<!-- Instrucciones del ejercicio: copia desde aquí hasta la rúbrica -->

Construye un plugin de servidor que responda a `/dado` con resultados de dados, con núcleo probado y repositorio documentado.

### Punto de partida

Tu proyecto Git de las lecciones anteriores, con el núcleo Java, sus pruebas, el adaptador Hytale y el `manifest.json`. El adaptador ya compila y se empaqueta en el ejemplo, pero la carga y la respuesta en el juego dependen de tu prueba: no envíes como completo un núcleo aislado.

### Pasos

1. Implementa `/dado` como `1d6`, y `/dado 2d6` con los dos valores y el total. Acepta `d20`. Valida de 1 a 20 dados y de 2 a 100 caras; muestra cómo corregir entradas inválidas. **Comprueba:** el núcleo no importa clases de Hytale.
2. Ejecuta las pruebas Java de L5. **Comprueba:** terminan con `Pruebas del núcleo: OK` y el proceso no informa una excepción.
3. Compila el plugin con el procedimiento de L6 (compilación y empaquetado comprobados en el ejemplo) y pruébalo en un servidor aislado en tu máquina, sin abrir puertos, con autenticación oficial. **Comprueba:** que el JAR contiene `manifest.json` en la raíz y que todas las filas de la tabla de L6, incluido el argumento extra, se observaron en el juego. Registra resultados reales.
4. Completa README y licencia: propósito, instrucciones repetibles, versión exacta de juego y API, JDK, comandos de compilación e instalación, pruebas y fecha. **Comprueba:** no incluye credenciales, recursos, JAR ni mundo del juego.
5. Haz commits explicativos y crea la etiqueta `v0.1.0` después de la última corrección; súbela junto con la rama. **Comprueba:** la etiqueta aparece en tu repositorio público y apunta al commit final.

### Qué entregar

- URL HTTPS de tu repositorio público en GitHub, GitLab, Bitbucket o Codeberg.
- Versión del juego y entorno de modding que realmente usaste, elegidos en el formulario.
- En el comentario: etiqueta `v0.1.0`, fecha de prueba y una decisión propia o dificultad explicada en dos o tres frases.

El tutor revisa que funcione en la versión declarada, las pruebas, Git, README y alcance. Si pide cambios, haz un commit, una etiqueta nueva como `v0.1.1` y reenvía sin mover la anterior.

### Antes de enviar

- Las pruebas Java pasan y se puede repetir su ejecución.
- El JAR se arma desde las fuentes con `manifest.json` en la raíz y sin archivos del juego.
- Los casos de L6 se observaron en el juego y las versiones corresponden al proyecto.
- El README explica compilación, instalación local, uso y retirada del plugin.
- El repositorio no contiene archivos de juego, binarios, mundos, credenciales ni configuraciones privadas.
- La etiqueta indicada existe y el enlace del repositorio funciona sin iniciar sesión.

## Rúbrica

| Orden | Criterio | Qué se revisa |
|---|---|---|
| 1 | Funciona en la versión declarada | En la etiqueta indicada, compila con las versiones documentadas y la prueba local reproduce los casos válidos, inválidos y argumento extra de L6; las versiones coinciden con la entrega. |
| 2 | Núcleo con pruebas | Las pruebas de L5 pasan; cubren notación, límites, número grande, rango, cantidad, suma y secuencia determinista; el núcleo no importa API Hytale. |
| 3 | Uso de Git | Hay commits pequeños comprensibles y etiqueta subida. No se incluyen binarios, archivos del juego, mundos, credenciales ni resultados generados. |
| 4 | README y licencia | Explica uso, compilación, pruebas, instalación y retirada, versiones realmente probadas, fecha y licencia compatible para las fuentes propias. |
| 5 | Alcance y comprensión | Implementa lo pedido sin código ajeno sin licencia; la explicación de una decisión o dificultad corresponde al proyecto. |
