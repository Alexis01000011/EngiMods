# 0003. Hosting de staging

- Estado: Aceptada
- Fecha: 2026-11-03 (actualizada y aceptada el 2026-11-05)
- Historia: EM-005

## Contexto

Staging debe ejecutar Django 5.2 y PostgreSQL, servir estáticos con HTTPS y permitir
repetir despliegue, respaldo y restauración. El piloto completo tiene un límite
de MXN 1,500, compartido con correo y dominio. Son tres personas; falta definir
quién administra la infraestructura y si todas necesitan acceso al proveedor.

Es un proyecto escolar: staging sirve para la demostración de la entrega de
semestre (alrededor del 1 de diciembre de 2026) con Stripe en modo prueba. El
equipo prefiere la opción más ligera y barata que cumpla EM-005.

## Opciones consideradas

Precios de Render y Railway consultados el 2026-11-03 en fuentes oficiales.
Importes en USD por mes, antes de impuestos, cambio de moneda, dominio y
excedentes. **El tipo de cambio y el importe final en MXN están sin verificar.**
`T` representa los MXN por USD aplicados al cobro: no es una cotización ni un
tipo de cambio supuesto.

| Opción | USD/mes y equivalente MXN | Límites y operación |
|---|---|---|
| Render con servicios gratuitos | USD 0 / MXN 0 | La web se suspende tras 15 minutos sin tráfico y PostgreSQL gratuito vence a los 30 días. Sirve para explorar; puede interrumpir la demostración y requiere plan de salida antes del vencimiento. |
| Render gratuito (solo web) con PostgreSQL gratuito de Neon | USD 0 / MXN 0 | La web de Render tiene los mismos límites de la fila anterior, pero la base vive en Neon y no depende del vencimiento de 30 días de Render. La conexión es por `DATABASE_URL`, que el proyecto ya usa. Los límites del plan gratuito de Neon se consultaron el 2026-11-05 y la suspensión por inactividad, la región y el historial de restauración se verificaron el 2026-11-09; ambos están en Consecuencias. |
| Render con web y PostgreSQL pagados | USD 13 de base = `13 × T` MXN; para workspace Pro, USD 38 = `38 × T` MXN | Web de 512 MB: USD 7; PostgreSQL de 256 MB: USD 6. Hobby tiene un asiento y cuesta USD 0 de workspace; Pro cuesta USD 25 y admite asientos ilimitados. Son bases, no topes de factura. |
| Railway | Hobby: mínimo USD 5 = `5 × T` MXN; Pro: mínimo USD 20 = `20 × T` MXN | El mínimo incluye crédito de consumo; CPU, memoria, volumen y salida se cobran por uso y pueden superarlo. Pro anuncia asientos ilimitados. La prueba gratuita ofrece USD 5 por 30 días; no es infraestructura gratuita permanente para el piloto. |
| Vercel | Sin verificar | Ejecuta Python como funciones sin servidor, no como un proceso de Django que se queda vivo. No incluye PostgreSQL (habría que sumar otro proveedor) ni un paso natural para `migrate`, y el build tendría que compilar Tailwind y correr `collectstatic`. Que el plan gratuito sea solo para uso no comercial está sin verificar; importaría si el piloto cobra dinero real. |

Fuentes: [precios de Render](https://render.com/pricing),
[limitaciones gratuitas de Render](https://render.com/docs/free),
[precios de Railway](https://railway.com/pricing),
[precios de Neon](https://neon.com/pricing) (sin consultar) y
[plan Hobby de Vercel](https://vercel.com/docs/plans/hobby) (sin consultar).
Los precios de Render se comprobaron también en su página renderizada en
navegador, porque su extracción de texto inicial no mostraba las tablas de
cómputo.

Render tiene [guía oficial de Django y PostgreSQL](https://render.com/docs/deploy-django);
Railway tiene [guía de Django y PostgreSQL](https://railway.com/guides/django).
Ambos son compatibles con el stack del ADR 0001 y permiten avanzar EM-005 y,
después, EM-008. No se presupone que una guía sustituya nuestros criterios.

## Decisión

**Se elige Render gratuito para la web y Neon gratuito para PostgreSQL**,
decidido por el equipo el 2026-11-05.

- Cuesta MXN 0 y deja el presupuesto del piloto para dominio y correo.
- Render corre Django como un servidor normal y tiene guía oficial; Neon evita
  el vencimiento de 30 días del PostgreSQL gratuito de Render.
- La suspensión de la web tras 15 minutos sin tráfico es aceptable para una
  demostración escolar: se abre el sitio unos minutos antes de presentar.
- Se descarta Vercel porque obliga a adaptar Django a funciones sin servidor y
  a contratar la base aparte, sin ahorrar nada frente a esta opción.
- Si el piloto recibe alumnos o dinero reales, se pasa la web a un plan pagado
  de Render sin cambiar código, solo el plan del servicio.

## Consecuencias

- Antes de crear los servicios, quien haga EM-005 consulta en neon.com los
  límites del plan gratuito y los anota aquí con la fecha de consulta. Si
  alguno impide cumplir EM-005 (por ejemplo, borra bases inactivas antes del
  1 de diciembre), se vuelve a llevar la decisión al equipo.
- **Plan gratuito de Neon, consultado el 2026-11-05** en
  [neon.com/pricing](https://neon.com/pricing) (transcrito por el equipo):
  USD 0, "sin límite de tiempo" y sin tarjeta; hasta 100 proyectos; 100 CU-hrs
  al mes por proyecto; 1 GB de almacenamiento por proyecto; tamaños de hasta
  2 CU (8 GB de RAM); miembros de equipo ilimitados. Alcanza para staging: no
  vence y la base de la demostración ocupa muy por debajo de 1 GB.
  Importa que la base se suspenda sola: una base de 0.25 CU encendida todo el
  mes gasta unas 182 CU-hrs (0.25 × 730 h), más que las 100 del plan.
- **Verificado al crear staging, el 2026-11-09** (EM-005), en la consola de
  Neon: la base se suspende tras 5 minutos sin actividad (*scale to zero*),
  activo y no configurable en el plan gratuito; el historial para restaurar a
  un momento anterior es de 6 horas. La base está en AWS US East 2 (Ohio) y la
  web de Render en Ohio. Respaldo y restauración probados con `pg_dump` en
  `docs/despliegue.md`.
- Una persona designada administra las cuentas de Render y Neon; no se
  comparten contraseñas. Si más personas necesitan acceso, se invitan como
  miembros cuando el plan lo permita.
- Elegir en Neon una región cercana a la de Render para no sumar latencia.
- EM-005 debe probar el despliegue con `DEBUG=False`, configurar HTTPS y cookies
  seguras según el proxy, y ejecutar `check --deploy`. El build compila Tailwind
  (ADR 0002) y corre `collectstatic`; las migraciones corren en cada despliegue.
- La migración a otro proveedor seguirá siendo viable mediante código, variables
  y `pg_dump`/restauración; los detalles se documentarán en `docs/despliegue.md`.
- Respaldar fuera de la instancia y demostrar una restauración sigue siendo un
  criterio obligatorio. PostgreSQL y archivos del alumno no vivirán en el disco
  efímero de la web. No hacen falta Redis, workers ni almacenamiento de archivos
  para dar por satisfecha esta decisión.
- EM-008 (correo) sigue pendiente del ADR 0004. Antes de aceptarlo, revisar si
  el plan gratuito de Render permite SMTP saliente; si no, usar la API HTTPS
  del proveedor de correo.
