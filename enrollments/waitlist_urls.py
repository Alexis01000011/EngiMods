from django.urls import path

from . import views

app_name = "waitlist"

urlpatterns = [
    path("", views.join_waitlist, name="join"),
]
