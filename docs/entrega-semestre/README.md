# EngiMods: guía de entrega

Entrega del semestre agosto–diciembre 2026. El 18 de noviembre de 2026, con hora por confirmar.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `tecnico.md` | Documento técnico; fuente del PDF. |
| `tecnico.pdf` | Versión de lectura del documento técnico. |
| `evidencias.md` | Evidencias de Fabián, por PR. |
| `negocio.md` | Modelo de negocio, Canvas, viabilidad y plan de marketing. |
| `presentacion.md` | Presentación completa con las secciones de cada integrante. |
| `exportar_pdf.py` | Programa auxiliar que convierte Markdown a PDF. |
| `README.md` | Esta guía. |

## Generar los PDF

```bash
python3 docs/entrega-semestre/exportar_pdf.py docs/entrega-semestre/tecnico.md
python3 docs/entrega-semestre/exportar_pdf.py docs/entrega-semestre/negocio.md
python3 docs/entrega-semestre/exportar_pdf.py docs/entrega-semestre/presentacion.md
```

Requiere Python 3, ReportLab y Markdown. Usa tamaño Carta, márgenes de 2.54 cm y fuente de 11 puntos.

## Checklist antes de entregar

- [ ] Los tres PDF existen, abren y son coherentes con sus fuentes.
- [ ] La presentación tiene los guiones de Pedro, Fabián y Alexis.
- [ ] Las capturas de staging están tomadas (si se incluyen).
- [ ] La demo está ensayada o sus límites están documentados.
- [ ] La exposición está repartida y el envío tiene comprobante.

## Reparto de la exposición

| Integrante | Sección |
|---|---|
| Pedro | Diapositivas 1–6 (problema, valor, canvas, oferta, recorrido), 8 (sus aportaciones), 11–13 (marketing, métricas, próximos pasos) |
| Fabián | Diapositiva 9 (sus aportaciones) y apoyo en la 7 (arquitectura) |
| Alexis | Diapositiva 10 (sus aportaciones) y la demo en vivo si se acuerda |

El reparto es una propuesta; el equipo lo confirma.

## Pendientes de staging

Observados el 16 de noviembre en páginas públicas: registro bloqueado por falta de aviso de privacidad vigente, páginas legales con 404, un curso ficticio sin temario publicado. El equipo debe verificar si esas condiciones cambiaron. No se inventan textos legales para llenar esos huecos.
