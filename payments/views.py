import logging
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from courses.models import Course
from enrollments.models import Enrollment

from .models import Payment

logger = logging.getLogger(__name__)


class Blocker:
    """Por qué no se puede pagar un curso. Cada caso tiene su texto en la plantilla."""

    HAS_ACCESS = "has_access"
    COHORT_COURSE = "cohort_course"
    UNVERIFIED_EMAIL = "unverified_email"
    UNAVAILABLE = "unavailable"


def has_access(user, course):
    return Enrollment.objects.with_access().filter(user=user, course=course).exists()


def checkout_blocker(user, course):
    """El motivo por el que `user` no puede pagar `course`, o None si sí puede."""
    if has_access(user, course):
        return Blocker.HAS_ACCESS
    # Un curso por grupos se paga para un grupo; los grupos llegan con EM-050.
    if course.kind == Course.Kind.COURSE:
        return Blocker.COHORT_COURSE
    if not user.can_pay:
        return Blocker.UNVERIFIED_EMAIL
    if not settings.STRIPE_SECRET_KEY:
        return Blocker.UNAVAILABLE
    return None


def create_checkout_session(request, course):
    """Sesión de Stripe Checkout con el precio del curso guardado en la base de datos."""
    client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)
    success_url = request.build_absolute_uri(reverse("payments:success", args=[course.slug]))
    return client.v1.checkout.sessions.create(
        params={
            "mode": "payment",
            # Sin payment_method_types: la API de Stripe ya no lo acepta en Checkout y los
            # métodos de pago se eligen en el Dashboard (docs/stripe.md, Reglas).
            "line_items": [
                {
                    "quantity": 1,
                    "price_data": {
                        "currency": "mxn",
                        "unit_amount": course.price_cents,
                        "product_data": {"name": course.title},
                    },
                }
            ],
            "customer_email": request.user.email,
            "client_reference_id": str(request.user.pk),
            "metadata": {"user_id": str(request.user.pk), "course_id": str(course.pk)},
            "locale": "es-419",
            # Stripe reemplaza {CHECKOUT_SESSION_ID}; por eso no pasa por reverse().
            "success_url": f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": request.build_absolute_uri(
                reverse("payments:cancel", args=[course.slug])
            ),
        }
    )


@login_required
def checkout(request, slug):
    """Confirmar y pagar (EM-042). GET muestra el resumen; POST abre Stripe Checkout."""
    course = get_object_or_404(Course.objects.published().select_related("game"), slug=slug)
    blocker = checkout_blocker(request.user, course)
    if request.method == "POST" and blocker is None:
        try:
            session = create_checkout_session(request, course)
        except stripe.StripeError as error:
            # Solo el tipo de error: el mensaje de Stripe puede traer datos de la petición.
            logger.warning(
                "Stripe no abrió el Checkout del curso %s: %s", course.pk, type(error).__name__
            )
            messages.error(
                request,
                _("No se pudo abrir el pago. No se hizo ningún cargo; intenta de nuevo."),
            )
            return redirect("payments:checkout", slug=course.slug)
        Payment.objects.create(
            user=request.user,
            course=course,
            amount_cents=course.price_cents,
            stripe_checkout_session_id=session.id,
        )
        # 303: el navegador va a Stripe con GET, como pide su documentación.
        return HttpResponseRedirect(session.url, status=303)
    return render(
        request,
        "payments/checkout.html",
        {
            "course": course,
            "price": Decimal(course.price_cents) / 100,
            "blocker": blocker,
        },
        status=400 if request.method == "POST" else 200,
    )


@login_required
def checkout_success(request, slug):
    """Página de regreso desde Stripe. No inscribe: eso lo hace el webhook (EM-043)."""
    course = get_object_or_404(Course.objects.published(), slug=slug)
    payment = Payment.objects.filter(
        user=request.user,
        course=course,
        stripe_checkout_session_id=request.GET.get("session_id", ""),
    ).first()
    return render(
        request,
        "payments/success.html",
        {"course": course, "payment": payment, "has_access": has_access(request.user, course)},
    )


@login_required
def checkout_cancel(request, slug):
    """Página de regreso si la persona cancela en Stripe."""
    course = get_object_or_404(Course.objects.published(), slug=slug)
    return render(request, "payments/cancel.html", {"course": course})
