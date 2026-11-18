# Textos legales para staging (demostración)

Estos textos son placeholders para desbloquear el registro en staging y poder hacer la demo. No son textos legales reales ni sustituyen la revisión de un responsable legal.

## Cómo cargarlos

1. Abre el admin de staging: `https://engimods-staging.onrender.com/admin/`
2. Inicia sesión con la cuenta de superusuario.
3. Ve a **Core → Textos legales → Agregar texto legal**.
4. Crea **dos** registros con los datos de abajo.

### Registro 1: Aviso de privacidad

| Campo | Valor |
|---|---|
| Tipo | Aviso de privacidad |
| Versión | 0.1 |
| Vigente desde | 2026-11-17 |
| Texto | (copiar el bloque de abajo) |

```
Aviso de privacidad — versión provisional para demostración

Este aviso es un documento provisional utilizado exclusivamente en el entorno de pruebas (staging) de EngiMods. No constituye un aviso de privacidad legal vigente.

Responsable

EngiMods (proyecto académico del Equipo 8, Negocios Electrónicos, Universidad Autónoma de Zacatecas). Responsable legal por definir.

Datos que se recopilan

Correo electrónico: para crear la cuenta e iniciar sesión.
Nombre a mostrar: para identificarte dentro de la plataforma.
Datos de navegación: páginas visitadas y acciones dentro del sitio, con fines de mejora del servicio.

Datos que no se recopilan

EngiMods no almacena datos de tarjeta de crédito ni información financiera. Los pagos se procesan a través de Stripe, que opera como procesador de pagos independiente bajo sus propios términos.

Finalidad

Los datos se utilizan para operar la plataforma: registro, acceso al contenido, seguimiento del avance y revisión de entregas.

Derechos

Puedes solicitar la eliminación de tu cuenta y tus datos enviando un correo al administrador del proyecto. El procedimiento formal de derechos ARCO se definirá cuando el proyecto tenga un responsable legal.

Cambios

Este aviso puede actualizarse. La versión vigente siempre estará disponible en /privacidad/.

Última actualización: 17 de noviembre de 2026.
```

### Registro 2: Términos y condiciones y política de devolución

| Campo | Valor |
|---|---|
| Tipo | Términos y condiciones y política de devolución |
| Versión | 0.1 |
| Vigente desde | 2026-11-17 |
| Texto | (copiar el bloque de abajo) |

```
Términos y condiciones y política de devolución — versión provisional para demostración

Estos términos son un documento provisional utilizado exclusivamente en el entorno de pruebas (staging) de EngiMods. No constituyen un contrato legal vigente.

Qué es EngiMods

EngiMods es una academia en línea en español para aprender a crear mods de videojuegos con prácticas de ingeniería de software. Es un proyecto académico del Equipo 8 de Negocios Electrónicos de la Universidad Autónoma de Zacatecas.

Acceso al contenido

Al pagar un curso, obtienes acceso al contenido por el número de días indicado en la página del curso. El acceso comienza desde el momento de la inscripción. El contenido es para uso personal y no puede redistribuirse.

Pagos

Los pagos se procesan a través de Stripe en modo de prueba. En esta etapa no se realizan cobros reales. Cuando el proyecto opere comercialmente, los pagos se procesarán en pesos mexicanos (MXN) a través de Stripe.

Política de devolución

Durante el periodo de demostración no se realizan cobros, por lo que no aplican devoluciones. Para la operación comercial futura, la política de devolución se definirá antes de aceptar pagos reales, conforme a la Ley Federal de Protección al Consumidor.

Entregas y contenido del alumno

Las entregas consisten en enlaces a repositorios públicos de código. EngiMods no almacena el código del alumno; solo guarda el enlace y la revisión del tutor. El alumno conserva la propiedad de su trabajo.

Conducta

El alumno se compromete a usar la plataforma con respeto. EngiMods puede suspender el acceso en caso de uso indebido.

Cambios

Estos términos pueden actualizarse. La versión vigente siempre estará disponible en /terminos/.

Última actualización: 17 de noviembre de 2026.
```

## Después de cargar

1. Verifica que `/privacidad/` y `/terminos/` ya no dan 404.
2. Verifica que `/registro/` ya permite crear una cuenta.
3. Para completar el registro, el correo de verificación sale en los logs de Render: Dashboard → engimods-staging → Logs. Busca el enlace que contiene `/verificar/`.
