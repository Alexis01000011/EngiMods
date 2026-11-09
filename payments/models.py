from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    """Cobro de un curso con Stripe Checkout (EM-042).

    Se crea en `pendiente` al abrir el Checkout. El webhook (EM-043) lo confirma con el
    monto que reporta Stripe; la página de éxito no cambia nada. El id de la sesión de
    Checkout es único y es la llave de idempotencia del webhook.
    """

    class Status(models.TextChoices):
        PENDING = "pending", _("Pendiente")
        PAID = "paid", _("Pagado")

    # PROTECT: no se borra historial de dinero (docs/arquitectura.md).
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name=_("alumno"),
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name=_("curso"),
    )
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.PENDING)
    amount_cents = models.PositiveIntegerField(
        _("monto en centavos"),
        help_text=_(
            "En MXN. Al abrir el pago es el precio del curso; al confirmarlo, lo que cobró Stripe."
        ),
    )
    stripe_checkout_session_id = models.CharField(
        _("id de la sesión de Checkout"), max_length=255, unique=True
    )
    created_at = models.DateTimeField(_("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(_("actualizado el"), auto_now=True)

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = _("pago")
        verbose_name_plural = _("pagos")

    def __str__(self):
        return f"{self.user} · {self.course} · {self.get_status_display()}"
