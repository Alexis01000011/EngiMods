"""Webhook de Stripe (EM-043). Los eventos se firman de verdad con un secreto de prueba."""

import hashlib
import hmac
import json
import time
from datetime import timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from catalog.models import Game
from courses.models import Course
from enrollments.models import Enrollment
from payments.models import Payment

pytestmark = pytest.mark.django_db

SECRET = "whsec_prueba"
SESSION_ID = "cs_test_123"


@pytest.fixture(autouse=True)
def webhook_secret(settings):
    settings.STRIPE_WEBHOOK_SECRET = SECRET


@pytest.fixture
def course():
    game = Game.objects.create(name="Juego", slug="juego", status=Game.Status.ACTIVE)
    return Course.objects.create(
        title="Misión Cero",
        slug="mision-cero",
        game=game,
        kind=Course.Kind.SHORT_PRACTICE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=1,
        price_cents=19900,
        access_days=30,
        status=Course.Status.PUBLISHED,
    )


@pytest.fixture
def student():
    return User.objects.create_user(
        email="alumna@example.com",
        password="una-clave-larga-42",
        display_name="Alumna",
        email_verified_at=timezone.now(),
    )


@pytest.fixture
def payment(student, course):
    return Payment.objects.create(
        user=student,
        course=course,
        amount_cents=course.price_cents,
        stripe_checkout_session_id=SESSION_ID,
    )


def make_event(event_type="checkout.session.completed", payment_status="paid", **session):
    return {
        "id": "evt_test_1",
        "object": "event",
        "type": event_type,
        "data": {
            "object": {
                "id": SESSION_ID,
                "object": "checkout.session",
                "payment_status": payment_status,
                "amount_total": 19900,
                **session,
            }
        },
    }


def signature(payload, secret=SECRET):
    timestamp = int(time.time())
    digest = hmac.new(secret.encode(), f"{timestamp}.{payload}".encode(), hashlib.sha256)
    return f"t={timestamp},v1={digest.hexdigest()}"


def send(client, event, secret=SECRET):
    payload = json.dumps(event)
    return client.post(
        reverse("stripe_webhook"),
        payload,
        content_type="application/json",
        headers={"Stripe-Signature": signature(payload, secret)},
    )


# Firma y método


def test_la_ruta_es_la_documentada():
    assert reverse("stripe_webhook") == "/pagos/stripe/webhook/"


def test_firma_invalida_da_400_y_no_cambia_nada(client, payment):
    response = send(client, make_event(), secret="whsec_otro")
    assert response.status_code == 400
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PENDING
    assert not Enrollment.objects.exists()


def test_sin_cabecera_de_firma_da_400(client, payment):
    response = client.post(
        reverse("stripe_webhook"), json.dumps(make_event()), content_type="application/json"
    )
    assert response.status_code == 400
    assert not Enrollment.objects.exists()


def test_payload_que_no_es_json_da_400(client):
    payload = "esto no es json"
    response = client.post(
        reverse("stripe_webhook"),
        payload,
        content_type="application/json",
        headers={"Stripe-Signature": signature(payload)},
    )
    assert response.status_code == 400


def test_get_da_405(client):
    assert client.get(reverse("stripe_webhook")).status_code == 405


def test_sin_secreto_configurado_da_500(client, settings, payment):
    settings.STRIPE_WEBHOOK_SECRET = ""
    assert send(client, make_event(), secret="").status_code == 500
    assert not Enrollment.objects.exists()


def test_no_exige_csrf(payment):
    assert send(Client(enforce_csrf_checks=True), make_event()).status_code == 200


# Pago confirmado


def test_pago_confirmado_inscribe_con_fin_de_acceso(client, payment, student, course):
    assert send(client, make_event()).status_code == 200
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PAID
    enrollment = Enrollment.objects.get()
    assert enrollment.user == student
    assert enrollment.course == course
    assert enrollment.origin == Enrollment.Origin.STRIPE
    assert enrollment.status == Enrollment.Status.ACTIVE
    assert enrollment.access_ends_at == enrollment.enrolled_at + timedelta(days=30)
    assert Enrollment.objects.with_access().filter(user=student, course=course).exists()


def test_el_monto_sale_de_amount_total_no_del_precio_del_curso(client, payment, course):
    course.price_cents = 99900
    course.save()
    send(client, make_event(amount_total=15000))
    payment.refresh_from_db()
    assert payment.amount_cents == 15000


def test_el_mismo_evento_dos_veces_no_duplica(client, payment):
    send(client, make_event())
    assert send(client, make_event()).status_code == 200
    assert Payment.objects.filter(status=Payment.Status.PAID).count() == 1
    assert Enrollment.objects.count() == 1


def test_pago_ya_confirmado_no_cambia_el_monto(client, payment):
    send(client, make_event(amount_total=15000))
    send(client, make_event(amount_total=1))
    payment.refresh_from_db()
    assert payment.amount_cents == 15000


# Eventos que no inscriben


def test_completed_unpaid_no_cambia_nada(client, payment):
    assert send(client, make_event(payment_status="unpaid")).status_code == 200
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PENDING
    assert not Enrollment.objects.exists()


def test_async_payment_succeeded_no_se_maneja_todavia(client, payment):
    response = send(client, make_event(event_type="checkout.session.async_payment_succeeded"))
    assert response.status_code == 200
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PENDING
    assert not Enrollment.objects.exists()


def test_otro_tipo_de_evento_da_200(client, payment):
    assert send(client, make_event(event_type="charge.refunded")).status_code == 200
    assert not Enrollment.objects.exists()


def test_sesion_desconocida_da_200_y_no_crea_nada(client, student, course):
    assert send(client, make_event()).status_code == 200
    assert not Payment.objects.exists()
    assert not Enrollment.objects.exists()


# Alumno con inscripciones previas


def test_con_acceso_vigente_el_pago_queda_pagado_sin_otra_inscripcion(
    client, payment, student, course
):
    existing = Enrollment.objects.create(
        user=student, course=course, origin=Enrollment.Origin.SCHOLARSHIP
    )
    ends_at = existing.access_ends_at
    assert send(client, make_event()).status_code == 200
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PAID
    assert payment.amount_cents == 19900
    assert Enrollment.objects.count() == 1
    existing.refresh_from_db()
    assert existing.access_ends_at == ends_at
    assert existing.origin == Enrollment.Origin.SCHOLARSHIP


def test_con_inscripcion_vencida_se_crea_la_nueva(client, payment, student, course):
    Enrollment.objects.create(
        user=student,
        course=course,
        origin=Enrollment.Origin.SCHOLARSHIP,
        enrolled_at=timezone.now() - timedelta(days=60),
    )
    send(client, make_event())
    assert Enrollment.objects.count() == 2
    assert Enrollment.objects.with_access().filter(origin=Enrollment.Origin.STRIPE).count() == 1


def test_con_inscripcion_cancelada_se_crea_la_nueva(client, payment, student, course):
    Enrollment.objects.create(
        user=student,
        course=course,
        origin=Enrollment.Origin.SCHOLARSHIP,
        status=Enrollment.Status.CANCELLED,
    )
    send(client, make_event())
    assert Enrollment.objects.with_access().filter(user=student, course=course).count() == 1


# Página de éxito


def test_la_pagina_de_exito_dice_inscrito_despues_del_webhook(client, payment, student, course):
    client.force_login(student)
    url = reverse("payments:success", args=[course.slug]) + f"?session_id={SESSION_ID}"
    assert "Listo, ya estás inscrito" not in client.get(url).content.decode()
    send(client, make_event())
    assert "Listo, ya estás inscrito" in client.get(url).content.decode()
