# Stripe en modo prueba

Cómo conectar tu copia local a Stripe en modo prueba y cómo recibir webhooks en local. El cobro (EM-042) y el webhook (EM-043) se construyen sobre esto.

## Reglas

- **Solo llaves de prueba** en desarrollo y staging: la secreta empieza con `sk_test_` y la publicable con `pk_test_`. Las llaves `sk_live_` no se usan hasta que el equipo decida abrir ventas reales (bloque B del recorte, en `docs/BACKLOG.md`).
- **Las llaves viven en `.env`** (local) o en las variables de entorno del proveedor (staging). Nunca en el código, en issues, en PR, en capturas ni en mensajes de Discord.
- **Nunca imprimas ni registres en logs** una llave, el secreto del webhook ni datos de tarjeta. Django ya oculta en sus páginas de error los settings cuyo nombre contiene `KEY` o `SECRET`; no lo rodees con `print(settings.STRIPE_SECRET_KEY)` ni nada parecido.
- El pre-commit del repo bloquea cualquier cosa que parezca una llave de Stripe. Si te bloquea, quita la llave; no lo desactives.
- Si una llave se filtró, aunque sea de prueba, revócala en el Dashboard (Desarrolladores, Claves de API, "Rotar clave") y avisa al equipo.
- **Métodos de pago: solo tarjeta y Link.** La API de Stripe ya no deja que el código elija los métodos de pago de Checkout; se activan en el Dashboard (Configuración, Pagos, Métodos de pago), por separado en modo prueba y en modo real. Deja activos solo tarjeta y Link (que paga con una tarjeta guardada) hasta EM-048: OXXO y otros métodos confirman el pago días después, y el webhook (EM-043) tiene que manejarlos antes de activarlos.

## 1. Obtener las llaves de prueba

1. Entra al [Dashboard de Stripe](https://dashboard.stripe.com/) con la cuenta del equipo. Si no tienes acceso, pídele a quien administra la cuenta que te invite; no crees una cuenta aparte.
2. Asegúrate de estar en **modo de prueba** (o en un *sandbox*, según cómo lo muestre el Dashboard).
3. Ve a **Desarrolladores → Claves de API** y copia la clave publicable y la clave secreta.

## 2. Configurar `.env`

Agrega a tu `.env` (las variables están descritas en `.env.example`):

```bash
STRIPE_SECRET_KEY=<tu clave secreta de prueba>
STRIPE_PUBLISHABLE_KEY=<tu clave publicable de prueba>
STRIPE_WEBHOOK_SECRET=<se obtiene en el paso 4>
```

Si las dejas vacías el sitio arranca igual; solo no funcionará el pago. Las pruebas automáticas no necesitan llaves.

## 3. Instalar Stripe CLI

Sigue la [guía oficial de instalación](https://docs.stripe.com/stripe-cli). En resumen:

- **Windows** con Scoop:
  ```bash
  scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
  scoop install stripe
  ```
  O descarga el `.zip` de la [página de versiones](https://github.com/stripe/stripe-cli/releases/latest) y agrega `stripe.exe` al `PATH`.
- **macOS:** `brew install stripe/stripe-cli/stripe`
- **Linux:** paquete `.deb`/`.rpm` o binario de la página de versiones.

Después vincúlala con la cuenta del equipo (abre el navegador para confirmar):

```bash
stripe login
```

## 4. Recibir webhooks en local

Con el servidor corriendo (`uv run python manage.py runserver`), en otra terminal:

```bash
stripe listen --forward-to localhost:8000/<ruta-del-webhook>/
```

- La ruta del webhook la define EM-043; cuando exista, usa la de su `urls.py`.
- Al arrancar, `stripe listen` imprime un secreto de firma que empieza con `whsec_`. Cópialo en `STRIPE_WEBHOOK_SECRET` de tu `.env` y reinicia el servidor. Ese secreto es de tu máquina y es distinto al del endpoint de staging.
- Deja `stripe listen` abierto mientras pruebas: si lo cierras, los eventos no llegan.

## 5. Disparar eventos de prueba

En una tercera terminal:

```bash
stripe trigger checkout.session.completed
stripe trigger checkout.session.async_payment_succeeded
```

En la terminal de `stripe listen` verás cada evento y la respuesta HTTP de tu servidor. Un `200` significa que tu webhook lo aceptó; un `400` suele ser firma inválida (revisa `STRIPE_WEBHOOK_SECRET`).

Los eventos de `stripe trigger` traen datos inventados por Stripe, así que no corresponden a pagos ni cursos de tu base. Para probar el flujo completo, haz un pago real de prueba desde el sitio (cuando exista EM-042) con estas tarjetas:

| Caso | Tarjeta |
|---|---|
| Pago aprobado | `4242 4242 4242 4242` |
| Requiere autenticación (3D Secure) | `4000 0025 0000 3155` |
| Pago rechazado | `4000 0000 0000 0002` |

Usa cualquier fecha futura, cualquier CVC de tres dígitos y cualquier código postal. Más casos en la [documentación de pruebas de Stripe](https://docs.stripe.com/testing).

## 6. Staging

En staging (EM-005) no se usa Stripe CLI: se registra un endpoint en **Desarrolladores → Webhooks** del Dashboard apuntando a la URL pública del webhook, y su secreto de firma se guarda en `STRIPE_WEBHOOK_SECRET` del proveedor de hosting.
