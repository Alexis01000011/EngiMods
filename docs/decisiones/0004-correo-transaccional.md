# 0004. Correo transaccional

- Estado: Propuesta
- Fecha: 2026-11-03
- Historia: EM-008

## Contexto

Registro, recuperación de contraseña y compra necesitan correo transaccional.
En desarrollo ya existe el backend de consola. EM-008 depende del staging de
EM-005 y requiere dominio con SPF/DKIM y pruebas en Gmail y Outlook. El dominio
y su administración DNS siguen sin definirse; son necesarios aunque el envío
sea gratuito. El gasto total del piloto no puede superar MXN 1,500.

## Opciones consideradas

Fuentes oficiales consultadas el 2026-11-03. Costos mensuales del envío, sin
dominio ni impuestos. En planes pagados, `T` es el tipo de cambio MXN/USD del
cobro, **sin verificar**; no se presenta una conversión numérica inventada.

| Opción | Costo | Límites e integración |
|---|---|---|
| Consola de Django | MXN 0 / USD 0 | Mantener en desarrollo. No entrega mensajes a alumnos y no satisface EM-008. |
| Resend Free | MXN 0 / USD 0 | 3,000 correos al mes, 100 al día y tres dominios. API y SMTP; requiere dominio verificado. Pro cuesta USD 20/mes (`20 × T` MXN) para 50,000 correos; no es necesario contratarlo para evaluar Free. |
| Brevo Free | MXN 0 / USD 0 | 300 envíos diarios, sin acumular los no usados; incluye correo transaccional. Ofrece API y SMTP. Revisar límites y marca del plan antes de elegirlo. |

Fuentes: [precios de Resend](https://resend.com/pricing),
[SMTP de Resend](https://resend.com/docs/send-with-smtp),
[dominios verificados de Resend](https://resend.com/docs/dashboard/domains/introduction),
[planes de Brevo](https://help.brevo.com/hc/en-us/articles/208589409-About-Brevo-s-pricing-plans) y
[correo transaccional de Brevo](https://www.brevo.com/products/transactional-email/).
Las cuotas mensuales de Resend se comprobaron en la página renderizada en navegador.

Ambos proveedores permiten avanzar EM-008 y luego los correos de EM-030,
EM-031 y EM-044. No dependen de PostgreSQL. El trabajo de configuración incluye
verificar dominio, cargar credenciales de entorno, probar entregabilidad y
documentar límites. No se prometen horas de implementación ni ausencia de spam.

Con SMTP permitido por el hosting se puede usar el backend de Django. Si el
proveedor de hosting restringe SMTP, evaluar API HTTPS o puertos admitidos antes
de implementar. La elección del transporte y cualquier dependencia adicional
deberán justificarse al concretar EM-008.

## Decisión

**Recomendación: evaluar Resend Free para el piloto**, siempre que 100 envíos
diarios cubran el registro y la operación previstos. Si el equipo necesita una
cuota diaria mayor, Brevo Free es la alternativa a contrastar. Ambas evitan un
costo de envío inicial; el dominio sigue teniendo costo propio.

**Falta la decisión del equipo.** No se crearon cuentas, verificaron dominios ni
enviaron correos externos. Hace falta confirmar proveedor, dominio, responsable
DNS, acceso del equipo y volumen esperado. No se comprarán planes al agotarse
una cuota sin que el equipo lo decida.

## Consecuencias

Al aceptar una opción, centralizar el envío en `core`, mantener consola en
desarrollo y documentar variables en `.env.example`. Conservar plantillas y
contenido dentro del proyecto facilita cambiar de proveedor.

Antes de cerrar EM-008, comprobar SPF/DKIM y entrega en Gmail y Outlook desde
staging. Los datos DNS exactos los da la cuenta del proveedor; no se inventan.
Registrar cuotas y comportamiento al llegar al límite, sin ocultar errores ni
guardar credenciales o contenido sensible en logs.
