from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
    path("privacidad/", views.privacy, name="privacy"),
    path("terminos/", views.terms, name="terms"),
]
