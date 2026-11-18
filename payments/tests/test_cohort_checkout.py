"""Pago de un grupo de curso (EM-050). Stripe se simula: las pruebas no usan llaves."""

import hashlib
import hmac
import json
import time
from datetime import date
from types import SimpleNamespace

import pytest
import stripe
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from catalog.models import Game
from cohorts.models import Cohort
from courses.models import Course
from enrollments.models import Enrollment
from payments.models import Payment

pytestmark = pytest.mark.django_db

SESSION_ID = "cs_test_grupo"
SESSION_URL = "https://checkout.stripe.com/c/pay/cs_test_grupo"
SECRET = "whsec_prueba"


class FakeStripe:
    def __init__(self):
        self.calls = []

    def __call__(self, api_key):
        sessions = SimpleNamespace(create=self.create)
        return SimpleNamespace(v1=SimpleNamespace(checkout=SimpleNamespace(sessions=sessions)))

    def create(self, params):
        self.calls.append(params)
        return SimpleNamespace(id=SESSION_ID, url=SESSION_URL)


@pytest.fixture
def fake_stripe(monkeypatch, settings):
    settings.STRIPE_SECRET_KEY = "sk_test_prueba"
    fake = FakeStripe()
    monkeypatch.setattr(stripe, "StripeClient", fake)
    return fake


@pytest.fixture
def game():
    return Game.objects.create(name="Juego", slug="juego", status=Game.Status.ACTIVE)


@pytest.fixture
def course(game):
    return Course.objects.create(
        title="Curso por grupos",
        slug="curso-por-grupos",
        game=game,
        kind=Course.Kind.COURSE,
        level=Course.Level.BEGINNER,
        description="Descripción.",
        requirements="Requisitos.",
        duration_weeks=6,
        price_cents=49900,
        access_days=10,
        status=Course.Status.PUBLISHED,
    )


@pytest.fixture
def cohort(course):
    return Cohort.objects.create(
        course=course,
        name="Grupo de noviembre",
        start_date=date(2026, 11, 23),
        end_date=date(2026, 12, 31),
        capacity=2,
        discord_url="https://discord.example.com/invitacion",
    )


@pytest.fixture
def student():
    return User.objects.create_user(
        email="alumna@example.com",
        password="una-clave-larga-42",
        display_name="Alumna",
        email_verified_at=timezone.now(),
    )


def checkout_url(course, cohort=None):
    url = reverse("payments:checkout", args=[course.slug])
    return f"{url}?grupo={cohort.pk}" if cohort else url


def test_se_paga_un_grupo_con_inscripcion_abierta(client, fake_stripe, course, cohort, student):
    client.force_login(student)

    response = client.post(checkout_url(course, cohort), {"grupo": cohort.pk})

    assert response.status_code == 303
    payment = Payment.objects.get()
    assert payment.cohort == cohort
    [params] = fake_stripe.calls
    assert params["metadata"]["cohort_id"] == str(cohort.pk)


def test_no_se_paga_un_grupo_cerrado(client, fake_stripe, course, cohort, student):
    cohort.status = Cohort.Status.CLOSED
    cohort.save()
    client.force_login(student)

    response = client.post(checkout_url(course, cohort), {"grupo": cohort.pk})

    assert response.status_code == 400
    assert "La inscripción de este grupo ya cerró." in response.content.decode()
    assert fake_stripe.calls == []
    assert not Payment.objects.exists()


def test_no_se_paga_un_grupo_lleno(client, fake_stripe, course, cohort, student):
    for index in range(cohort.capacity):
        Enrollment.objects.create(
            user=User.objects.create_user(email=f"lleno{index}@example.com", password="x-12345678"),
            course=course,
            cohort=cohort,
            origin=Enrollment.Origin.STRIPE,
        )
    client.force_login(student)

    response = client.post(checkout_url(course, cohort), {"grupo": cohort.pk})

    assert response.status_code == 400
    assert "El grupo está lleno." in response.content.decode()
    assert fake_stripe.calls == []
    assert not Payment.objects.exists()


def test_un_grupo_de_otro_curso_da_404(client, fake_stripe, game, course, student):
    other = Course.objects.create(
        title="Otro",
        slug="otro",
        game=game,
        kind=Course.Kind.COURSE,
        level=Course.Level.BEGINNER,
        description="x",
        requirements="x",
        duration_weeks=6,
        price_cents=10000,
        access_days=10,
        status=Course.Status.PUBLISHED,
    )
    other_cohort = Cohort.objects.create(
        course=other,
        name="Ajeno",
        start_date=date(2026, 11, 1),
        end_date=date(2026, 12, 1),
        capacity=2,
    )
    client.force_login(student)

    response = client.post(checkout_url(course, other_cohort), {"grupo": other_cohort.pk})

    assert response.status_code == 404
    assert fake_stripe.calls == []


def test_el_detalle_muestra_el_proximo_grupo_y_enlaza_al_pago(client, course, cohort):
    html = client.get(reverse("courses:course_detail", args=[course.slug])).content.decode()

    assert "Próximo grupo: Grupo de noviembre" in html
    assert "2 de 2 lugares disponibles." in html
    assert f"?grupo={cohort.pk}" in html
    assert "Inscribirme y pagar" in html


def test_el_detalle_no_ofrece_pagar_un_grupo_lleno(client, course, cohort):
    for index in range(cohort.capacity):
        Enrollment.objects.create(
            user=User.objects.create_user(email=f"lleno{index}@example.com", password="x-12345678"),
            course=course,
            cohort=cohort,
            origin=Enrollment.Origin.STRIPE,
        )

    html = client.get(reverse("courses:course_detail", args=[course.slug])).content.decode()

    assert "Este grupo está lleno." in html
    assert "Lista de espera" in html
    assert "Inscribirme y pagar" not in html


def signature(payload, secret=SECRET):
    timestamp = int(time.time())
    digest = hmac.new(secret.encode(), f"{timestamp}.{payload}".encode(), hashlib.sha256)
    return f"t={timestamp},v1={digest.hexdigest()}"


def test_el_webhook_inscribe_en_el_grupo(client, course, cohort, student, settings):
    settings.STRIPE_WEBHOOK_SECRET = SECRET
    payment = Payment.objects.create(
        user=student,
        course=course,
        cohort=cohort,
        amount_cents=course.price_cents,
        stripe_checkout_session_id=SESSION_ID,
    )
    event = {
        "id": "evt_grupo",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": SESSION_ID,
                "object": "checkout.session",
                "payment_status": "paid",
                "amount_total": 49900,
            }
        },
    }
    payload = json.dumps(event)

    response = client.post(
        reverse("stripe_webhook"),
        payload,
        content_type="application/json",
        headers={"Stripe-Signature": signature(payload)},
    )

    assert response.status_code == 200
    enrollment = Enrollment.objects.get()
    assert enrollment.cohort == cohort
    assert enrollment.user == student
    assert timezone.localtime(enrollment.access_ends_at).date() == date(2027, 1, 10)
    payment.refresh_from_db()
    assert payment.status == Payment.Status.PAID
