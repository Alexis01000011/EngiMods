# EngiMods: guía de revisión

El documento técnico y las evidencias están preparados para revisión; negocio y presentación siguen en borrador. La demostración no fue ensayada en esta revisión. La entrega es el 18 de noviembre de 2026, con hora por confirmar.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `tecnico.md` | Documento técnico; fuente del PDF. |
| `tecnico.pdf` | Versión de lectura del documento técnico. |
| `evidencias.md` | Evidencias del trabajo, por PR personales. |
| `negocio.md` | Borrador de negocio, costos, precios y marketing; falta cerrarlo. |
| `presentacion.md` | Borrador con la estructura y la sección de Fabián. |
| `exportar_pdf.py` | Programa auxiliar que convierte Markdown a PDF. |
| `README.md` | Esta guía. |

## El exportador de PDF

`exportar_pdf.py` es un programa auxiliar para regenerar el PDF a partir de Markdown; no forma parte de Django.

Desde la raíz del repositorio:

```bash
python3 docs/entrega-semestre/exportar_pdf.py docs/entrega-semestre/tecnico.md
```

Requiere Python 3, ReportLab y Markdown, disponibles en esta máquina; no agrega dependencias a la aplicación. Usa tamaño Carta, márgenes de 2.54 cm, fuente compatible con Arial de 11 puntos y no incluye encabezados ni pies.

## Revisar los cambios

La rama es `docs/entrega-semestre-18nov`, basada en `539f1e0`. Los siguientes comandos permiten revisar los cambios sin modificarlos:

```bash
git status -sb
git log --oneline main..HEAD
git diff --stat main...HEAD
git diff main...HEAD -- docs/entrega-semestre
```

## Relevo propuesto a Pedro

El siguiente reparto es una propuesta para Pedro y requiere su aceptación:

- Revisar y cerrar negocio y marketing en los nueve bloques del Canvas, con enfoque multijuego.
- Aportar sus propias evidencias.
- Preparar su parte de la exposición.
- Completar la presentación y, después de la revisión, exportar los PDF de negocio y presentación.
- Confirmar con Alexis y el equipo quién opera la infraestructura; ensayar una demostración con datos de prueba identificados o, si se afirma aprendizaje real, con un ejercicio probado.
- Hacer la revisión cruzada del documento técnico.
- Confirmar hora, canal, quién sube los archivos y el comprobante de envío.

## Pendientes observados en staging

El 16 de noviembre, en páginas públicas de staging, se observó el registro bloqueado, páginas legales con 404 y un curso ficticio sin temario publicado. No se volvió a comprobar: el equipo debe verificar si esas condiciones cambiaron, sin inferir el contenido privado.

No se deben inventar textos legales ni datos para llenar esos huecos. La evidencia comercial consta de una conversación y cuatro casos simulados, no cinco entrevistas reales; tampoco hay resultados comerciales medidos.

## Comprobaciones antes de publicar

Antes de publicar o enviar:

- [ ] Los tres PDF existen, abren y son coherentes con sus fuentes.
- [ ] La demostración está ensayada o sus límites quedan documentados.
- [ ] La exposición está repartida y el envío tiene comprobante.
