from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.register, name="register"),
    path("verificar/<uidb64>/<token>/", views.verify_email, name="verify_email"),
]
