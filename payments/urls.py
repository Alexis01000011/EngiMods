from django.urls import path

from . import views

app_name = "payments"

# Se monta bajo /cursos/: /cursos/<slug>/pagar/…
urlpatterns = [
    path("<slug:slug>/pagar/", views.checkout, name="checkout"),
    path("<slug:slug>/pagar/listo/", views.checkout_success, name="success"),
    path("<slug:slug>/pagar/cancelado/", views.checkout_cancel, name="cancel"),
]
