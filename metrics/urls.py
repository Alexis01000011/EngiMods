from django.urls import path

from . import views

app_name = "metrics"

urlpatterns = [
    path("", views.pilot, name="pilot"),
    path("csv/", views.pilot_csv, name="pilot_csv"),
]
