# 0003. Hosting de staging

- Estado: Propuesta
- Fecha: 2026-11-03
- Historia: EM-005

## Contexto

Staging debe ejecutar Django 5.2 y PostgreSQL, servir estáticos con HTTPS y permitir
repetir despliegue, respaldo y restauración. El piloto completo tiene un límite
de MXN 1,500, compartido con correo y dominio. Son tres personas; falta definir
quién administra la infraestructura y si todas necesitan acceso al proveedor.

## Opciones consideradas

Precios consultados el 2026-11-03 en fuentes oficiales. Importes en USD por mes,
antes de impuestos, cambio de moneda, dominio y excedentes. **El tipo de cambio
y el importe final en MXN están sin verificar.** `T` representa los MXN por USD
aplicados al cobro: no es una cotización ni un tipo de cambio supuesto.

| Opción | USD/mes y equivalente MXN | Límites y operación |
|---|---|---|
| Render con servicios gratuitos | USD 0 / MXN 0 | La web se suspende tras 15 minutos sin tráfico y PostgreSQL gratuito vence a los 30 días. Sirve para explorar; puede interrumpir la demostración y requiere plan de salida antes del vencimiento. |
| Render con web y PostgreSQL pagados | USD 13 de base = `13 × T` MXN; para workspace Pro, USD 38 = `38 × T` MXN | Web de 512 MB: USD 7; PostgreSQL de 256 MB: USD 6. Hobby tiene un asiento y cuesta USD 0 de workspace; Pro cuesta USD 25 y admite asientos ilimitados. Son bases, no topes de factura. |
| Railway | Hobby: mínimo USD 5 = `5 × T` MXN; Pro: mínimo USD 20 = `20 × T` MXN | El mínimo incluye crédito de consumo; CPU, memoria, volumen y salida se cobran por uso y pueden superarlo. Pro anuncia asientos ilimitados. La prueba gratuita ofrece USD 5 por 30 días; no es infraestructura gratuita permanente para el piloto. |

Fuentes: [precios de Render](https://render.com/pricing),
[limitaciones gratuitas de Render](https://render.com/docs/free) y
[precios de Railway](https://railway.com/pricing). Los precios de Render se
comprobaron también en su página renderizada en navegador, porque su extracción
de texto inicial no mostraba las tablas de cómputo.

Render tiene [guía oficial de Django y PostgreSQL](https://render.com/docs/deploy-django);
Railway tiene [guía de Django y PostgreSQL](https://railway.com/guides/django).
Ambos son compatibles con el stack del ADR 0001 y permiten avanzar EM-005 y,
después, EM-008. No se presupone que una guía sustituya nuestros criterios.

El trabajo de configuración es semejante: servidor de aplicación, controlador de
PostgreSQL, estáticos, variables, migraciones, seguridad HTTPS y documentación.
Railway añade seguimiento del consumo; Render exige escoger tamaños y revisar
capacidad. No se estiman horas sin datos del equipo.

## Decisión

**Recomendación: Render con web y PostgreSQL pagados para staging**, condicionada
a confirmar presupuesto y número de operadores. La base fija facilita planear
el gasto y evita la suspensión y caducidad del nivel gratuito. Hobby solo es
alternativa si una persona designada opera la cuenta; no se comparten contraseñas.
Si las tres necesitan acceso, comparar Render Pro con Railway Pro y su consumo.

**Falta la decisión del equipo.** No se han creado servicios ni contratado planes.
Antes de aceptar, registrar el costo convertido a MXN, impuestos y dominio,
meses de operación y excedentes previstos. Solo contratar si la suma del piloto
cabe en MXN 1,500; USD 13 no constituye una autorización de gasto.

## Consecuencias

Al aceptar una opción, EM-005 debe probar el despliegue con `DEBUG=False`,
configurar HTTPS y cookies seguras según el proxy, y ejecutar `check --deploy`.
La migración a otro proveedor seguirá siendo viable mediante código, variables
y `pg_dump`/restauración; los detalles se documentarán en `docs/despliegue.md`.

Respaldar fuera de la instancia y demostrar una restauración sigue siendo un
criterio obligatorio. PostgreSQL y archivos del alumno no vivirán en el disco
efímero de la web. No hacen falta Redis, workers ni almacenamiento de archivos
para dar por satisfecha esta decisión.
