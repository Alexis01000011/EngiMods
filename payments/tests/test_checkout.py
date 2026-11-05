"""Pago con Stripe Checkout (EM-042). Stripe se simula: las pruebas no usan llaves."""

from datetime import timedelta
from types import SimpleNamespace

import pytest
import stripe
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from catalog.models import Game
from courses.models import Course
from enrollments.models import Enrollment
from payments.models import Payment

pytestmark = pytest.mark.django_db

SESSION_ID = "cs_test_123"
SESSION_URL = "https://checkout.stripe.com/c/pay/cs_test_123"


class FakeStripe:
    """Sustituye a stripe.StripeClient y guarda lo que se le pidió."""

    def __init__(self, error=None):
        self.calls = []
        self.error = error

    def __call__(self, api_key):
        self.api_key = api_key
        sessions = SimpleNamespace(create=self.create)
        return SimpleNamespace(v1=SimpleNamespace(checkout=SimpleNamespace(sessions=sessions)))

    def create(self, params):
        self.calls.append(params)
        if self.error:
            raise self.error
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


def make_course(game, **changes):
    data = {
        "title": "Misión Cero",
        "slug": "mision-cero",
        "game": game,
        "kind": Course.Kind.SHORT_PRACTICE,
        "level": Course.Level.BEGINNER,
        "description": "Descripción.",
        "requirements": "Requisitos.",
        "duration_weeks": 1,
        "price_cents": 19900,
        "access_days": 30,
        "status": Course.Status.PUBLISHED,
        **changes,
    }
    return Course.objects.create(**data)


@pytest.fixture
def course(game):
    return make_course(game)


@pytest.fixture
def student():
    return User.objects.create_user(
        email="alumna@example.com",
        password="una-clave-larga-42",
        display_name="Alumna",
        email_verified_at=timezone.now(),
    )


def checkout_url(course):
    return reverse("payments:checkout", args=[course.slug])


# Al pagar se crea una sesión de Stripe Checkout con el precio del curso guardado en la base


def test_pagar_crea_la_sesion_con_el_precio_del_curso(client, fake_stripe, course, student):
    client.force_login(student)
    response = client.post(checkout_url(course))

    assert response.status_code == 303
    assert response.url == SESSION_URL
    assert fake_stripe.api_key == "sk_test_prueba"
    [params] = fake_stripe.calls
    assert params["mode"] == "payment"
    assert params["payment_method_types"] == ["card"]
    [item] = params["line_items"]
    assert item["quantity"] == 1
    assert item["price_data"]["currency"] == "mxn"
    assert item["price_data"]["unit_amount"] == 19900
    assert item["price_data"]["product_data"]["name"] == "Misión Cero"
    assert params["customer_email"] == "alumna@example.com"
    assert params["metadata"] == {"user_id": str(student.pk), "course_id": str(course.pk)}


def test_el_precio_sale_de_la_base_no_de_la_peticion(client, fake_stripe, course, student):
    course.price_cents = 29900
    course.save()
    client.force_login(student)
    client.post(checkout_url(course), {"price_cents": "1"})
    assert fake_stripe.calls[0]["line_items"][0]["price_data"]["unit_amount"] == 29900


def test_las_urls_de_regreso_son_de_este_curso(client, fake_stripe, course, student):
    client.force_login(student)
    client.post(checkout_url(course))
    params = fake_stripe.calls[0]
    success = reverse("payments:success", args=[course.slug])
    assert params["success_url"] == f"http://testserver{success}?session_id={{CHECKOUT_SESSION_ID}}"
    cancel = reverse("payments:cancel", args=[course.slug])
    assert params["cancel_url"] == f"http://testserver{cancel}"


def test_get_muestra_el_resumen_sin_llamar_a_stripe(client, fake_stripe, course, student):
    client.force_login(student)
    response = client.get(checkout_url(course))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Confirma tu inscripción" in html
    assert "MXN 199.00" in html
    assert "30 días desde que se confirma el pago" in html
    assert "Pagar con Stripe" in html
    assert fake_stripe.calls == []
    assert not Payment.objects.exists()


# Se registra un Pago pendiente ligado al alumno y al curso, con el id de sesión único


def test_se_registra_un_pago_pendiente(client, fake_stripe, course, student):
    client.force_login(student)
    client.post(checkout_url(course))

    payment = Payment.objects.get()
    assert payment.user == student
    assert payment.course == course
    assert payment.status == Payment.Status.PENDING
    assert payment.amount_cents == 19900
    assert payment.stripe_checkout_session_id == SESSION_ID


def test_el_id_de_la_sesion_es_unico(course, student):
    Payment.objects.create(
        user=student, course=course, amount_cents=100, stripe_checkout_session_id=SESSION_ID
    )
    with pytest.raises(IntegrityError):
        Payment.objects.create(
            user=student, course=course, amount_cents=100, stripe_checkout_session_id=SESSION_ID
        )


def test_un_pago_no_se_borra_con_el_curso(course, student):
    Payment.objects.create(
        user=student, course=course, amount_cents=100, stripe_checkout_session_id=SESSION_ID
    )
    with pytest.raises(ProtectedError):
        course.delete()


def test_si_stripe_falla_no_se_registra_pago(client, monkeypatch, settings, course, student):
    settings.STRIPE_SECRET_KEY = "sk_test_prueba"
    monkeypatch.setattr(stripe, "StripeClient", FakeStripe(error=stripe.APIConnectionError("x")))
    client.force_login(student)
    response = client.post(checkout_url(course), follow=True)
    assert not Payment.objects.exists()
    assert "No se pudo abrir el pago. No se hizo ningún cargo" in response.content.decode()


# Páginas de éxito y de cancelación en español


def test_la_pagina_de_exito_no_inscribe_y_explica_que_falta(client, course, student):
    Payment.objects.create(
        user=student, course=course, amount_cents=19900, stripe_checkout_session_id=SESSION_ID
    )
    client.force_login(student)
    url = reverse("payments:success", args=[course.slug])
    response = client.get(f"{url}?session_id={SESSION_ID}")
    assert response.status_code == 200
    html = response.content.decode()
    assert "Recibimos tu pago" in html
    assert "Stripe está confirmando el pago de Misión Cero." in html
    assert not Enrollment.objects.exists()
    assert Payment.objects.get().status == Payment.Status.PENDING


def test_la_pagina_de_exito_no_muestra_pagos_de_otra_persona(client, course, student):
    otra = User.objects.create_user(email="otra@example.com", password="x", display_name="Otra")
    Payment.objects.create(
        user=otra, course=course, amount_cents=19900, stripe_checkout_session_id=SESSION_ID
    )
    client.force_login(student)
    url = reverse("payments:success", args=[course.slug])
    html = client.get(f"{url}?session_id={SESSION_ID}").content.decode()
    assert "No encontramos ese pago" in html


def test_la_pagina_de_exito_dice_si_ya_quedo_inscrito(client, course, student):
    Enrollment.objects.create(user=student, course=course, origin=Enrollment.Origin.STRIPE)
    client.force_login(student)
    html = client.get(reverse("payments:success", args=[course.slug])).content.decode()
    assert "Listo, ya estás inscrito" in html


def test_la_pagina_de_cancelacion_dice_que_no_hubo_cargo(client, course, student):
    client.force_login(student)
    response = client.get(reverse("payments:cancel", args=[course.slug]))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Cancelaste el pago" in html
    assert "No se hizo ningún cargo." in html
    assert checkout_url(course) in html


@pytest.mark.parametrize("name", ["checkout", "success", "cancel"])
def test_las_paginas_de_pago_piden_sesion(client, course, name):
    response = client.get(reverse(f"payments:{name}", args=[course.slug]))
    assert response.status_code == 302
    assert response.url.startswith(reverse("accounts:login"))


def test_las_urls_estan_en_español(course):
    assert checkout_url(course) == "/cursos/mision-cero/pagar/"
    assert reverse("payments:success", args=[course.slug]) == "/cursos/mision-cero/pagar/listo/"
    assert reverse("payments:cancel", args=[course.slug]) == "/cursos/mision-cero/pagar/cancelado/"


# No se puede pagar un curso al que el alumno ya tiene acceso vigente


def test_con_acceso_vigente_no_se_puede_pagar(client, fake_stripe, course, student):
    Enrollment.objects.create(user=student, course=course, origin=Enrollment.Origin.SCHOLARSHIP)
    client.force_login(student)

    response = client.get(checkout_url(course))
    assert "Ya tienes acceso." in response.content.decode()
    assert "Pagar con Stripe" not in response.content.decode()

    response = client.post(checkout_url(course))
    assert response.status_code == 400
    assert fake_stripe.calls == []
    assert not Payment.objects.exists()


def test_con_acceso_vencido_si_se_puede_pagar(client, fake_stripe, course, student):
    Enrollment.objects.create(
        user=student,
        course=course,
        origin=Enrollment.Origin.STRIPE,
        enrolled_at=timezone.now() - timedelta(days=60),
    )
    client.force_login(student)
    response = client.post(checkout_url(course))
    assert response.status_code == 303
    assert Payment.objects.count() == 1


def test_con_inscripcion_cancelada_si_se_puede_pagar(client, fake_stripe, course, student):
    Enrollment.objects.create(
        user=student,
        course=course,
        origin=Enrollment.Origin.STRIPE,
        status=Enrollment.Status.CANCELLED,
    )
    client.force_login(student)
    assert client.post(checkout_url(course)).status_code == 303


def test_el_acceso_a_otro_curso_no_impide_pagar(client, fake_stripe, game, course, student):
    otro = make_course(game, title="Otro", slug="otro")
    Enrollment.objects.create(user=student, course=otro, origin=Enrollment.Origin.STRIPE)
    client.force_login(student)
    assert client.post(checkout_url(course)).status_code == 303


# Quién no puede pagar


def test_sin_correo_verificado_no_se_puede_pagar(client, fake_stripe, course, student):
    student.email_verified_at = None
    student.save()
    client.force_login(student)

    html = client.get(checkout_url(course)).content.decode()
    assert "Verifica tu correo para pagar." in html

    assert client.post(checkout_url(course)).status_code == 400
    assert fake_stripe.calls == []
    assert not Payment.objects.exists()


def test_un_curso_por_grupos_no_se_paga_todavia(client, fake_stripe, game, student):
    curso = make_course(game, slug="curso", kind=Course.Kind.COURSE, duration_weeks=6)
    client.force_login(student)
    html = client.get(checkout_url(curso)).content.decode()
    assert "Todavía no abre la inscripción." in html
    assert client.post(checkout_url(curso)).status_code == 400
    assert fake_stripe.calls == []


def test_sin_llave_de_stripe_no_se_intenta_cobrar(client, settings, monkeypatch, course, student):
    settings.STRIPE_SECRET_KEY = ""
    fake = FakeStripe()
    monkeypatch.setattr(stripe, "StripeClient", fake)
    client.force_login(student)
    html = client.get(checkout_url(course)).content.decode()
    assert "El pago no está disponible por ahora." in html
    assert client.post(checkout_url(course)).status_code == 400
    assert fake.calls == []


def test_un_curso_en_borrador_no_se_paga(client, fake_stripe, game, student):
    borrador = make_course(game, slug="borrador", status=Course.Status.DRAFT)
    client.force_login(student)
    assert client.get(checkout_url(borrador)).status_code == 404
    assert client.post(checkout_url(borrador)).status_code == 404


# Botón en el detalle del curso


def test_el_detalle_del_curso_tiene_el_boton_de_pago(client, course):
    html = client.get(reverse("courses:course_detail", args=[course.slug])).content.decode()
    assert "Inscribirme y pagar" in html
    assert checkout_url(course) in html


def test_con_acceso_el_detalle_no_ofrece_pagar(client, course, student):
    Enrollment.objects.create(user=student, course=course, origin=Enrollment.Origin.STRIPE)
    client.force_login(student)
    html = client.get(reverse("courses:course_detail", args=[course.slug])).content.decode()
    assert "Ya tienes acceso a este curso." in html
    assert "Inscribirme y pagar" not in html


def test_un_curso_por_grupos_no_muestra_el_boton(client, game):
    curso = make_course(game, slug="curso", kind=Course.Kind.COURSE, duration_weeks=6)
    html = client.get(reverse("courses:course_detail", args=[curso.slug])).content.decode()
    assert "Inscribirme y pagar" not in html


# Administración


def test_el_admin_lista_los_pagos_en_solo_lectura(admin_client, course, student):
    payment = Payment.objects.create(
        user=student, course=course, amount_cents=19900, stripe_checkout_session_id=SESSION_ID
    )
    response = admin_client.get(reverse("admin:payments_payment_changelist"))
    assert response.status_code == 200
    assert "alumna@example.com" in response.content.decode()
    assert admin_client.get(reverse("admin:payments_payment_add")).status_code == 403
    response = admin_client.get(reverse("admin:payments_payment_delete", args=[payment.pk]))
    assert response.status_code == 403
