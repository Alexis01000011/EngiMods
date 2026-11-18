from django.urls import path

from . import tutor_views

app_name = "clinics"

urlpatterns = [
    path("", tutor_views.sessions, name="sessions"),
]
