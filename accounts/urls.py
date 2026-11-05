from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("registro/", views.register, name="register"),
    path("registro/verificar/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("entrar/", views.LoginView.as_view(), name="login"),
    path("salir/", views.logout_view, name="logout"),
    path("privacidad/aceptar/", views.accept_privacy, name="accept_privacy"),
    path("recuperar-contrasena/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "recuperar-contrasena/enviado/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "recuperar-contrasena/listo/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "recuperar-contrasena/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
