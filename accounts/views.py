from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import (
    url_has_allowed_host_and_scheme,
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from core.emails import send_templated_email
from core.models import LegalText

from .forms import (
    LoginForm,
    NewPasswordForm,
    PasswordResetRequestForm,
    PrivacyAcceptForm,
    RegistrationForm,
)
from .models import PrivacyConsent, User
from .tokens import email_verification_token


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    path = reverse("accounts:verify_email", args=[uid, email_verification_token.make_token(user)])
    context = {
        "user": user,
        "verify_url": request.build_absolute_uri(path),
        "hours": settings.PASSWORD_RESET_TIMEOUT // 3600,
    }
    send_templated_email("verify_email", context, user.email)


def register(request):
    """Registro con correo (EM-030). Sin aviso de privacidad vigente no se abre."""
    if request.user.is_authenticated:
        messages.info(request, _("Ya tienes una sesión iniciada."))
        return redirect("enrollments:my_courses")
    privacy_notice = LegalText.objects.current(LegalText.Kind.PRIVACY)
    form = None
    if privacy_notice is not None:
        form = RegistrationForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            with transaction.atomic():
                user = form.save()
                PrivacyConsent.objects.create(user=user, legal_text=privacy_notice)
            send_verification_email(request, user)
            login(request, user)
            messages.success(
                request,
                _("Listo. Te enviamos un correo a %(email)s para verificar tu cuenta.")
                % {"email": user.email},
            )
            return redirect("enrollments:my_courses")
    return render(
        request, "accounts/register.html", {"form": form, "privacy_notice": privacy_notice}
    )


def verify_email(request, uidb64, token):
    """Marca el correo como verificado si el enlace es válido y no ha vencido."""
    try:
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or not email_verification_token.check_token(user, token):
        return render(request, "accounts/verify_email.html", {"verified": False}, status=400)
    if user.email_verified_at is None:
        user.email_verified_at = timezone.now()
        user.save(update_fields=["email_verified_at"])
    return render(request, "accounts/verify_email.html", {"verified": True})


def pending_privacy_notice(user):
    """Versión vigente del aviso de privacidad si el usuario aún no la acepta, o None."""
    notice = LegalText.objects.current(LegalText.Kind.PRIVACY)
    if notice is None or user.privacy_consents.filter(legal_text=notice).exists():
        return None
    return notice


def safe_next_url(request, url):
    """El destino de `next` si es de este sitio; si no, Mi panel."""
    if url and url_has_allowed_host_and_scheme(
        url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return url
    return resolve_url(settings.LOGIN_REDIRECT_URL)


class LoginView(auth_views.LoginView):
    """Inicio de sesión con correo (EM-031).

    Si el aviso de privacidad cambió de versión desde la última aceptación, antes de
    seguir pide aceptar la versión vigente (EM-033).
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        if pending_privacy_notice(self.request.user) is not None:
            query = urlencode({"next": self.get_success_url()})
            return redirect(f"{reverse('accounts:accept_privacy')}?{query}")
        return response


@require_POST
def logout_view(request):
    """Cierra la sesión. Solo por POST, para que un enlace ajeno no pueda sacarte."""
    logout(request)
    messages.info(request, _("Cerraste tu sesión. Vuelve cuando quieras."))
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def accept_privacy(request):
    """Aceptar la versión vigente del aviso de privacidad (EM-031, EM-033)."""
    next_url = safe_next_url(request, request.POST.get("next") or request.GET.get("next"))
    notice = pending_privacy_notice(request.user)
    if notice is None:
        return redirect(next_url)
    form = PrivacyAcceptForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        PrivacyConsent.objects.create(user=request.user, legal_text=notice)
        messages.success(
            request,
            _("Listo. Aceptaste el aviso de privacidad (versión %(version)s).")
            % {"version": notice.version},
        )
        return redirect(next_url)
    return render(
        request,
        "accounts/accept_privacy.html",
        {"form": form, "privacy_notice": notice, "next": next_url},
    )


class PasswordResetView(auth_views.PasswordResetView):
    """Pide el enlace de recuperación. Responde igual exista o no la cuenta."""

    template_name = "accounts/password_reset_form.html"
    form_class = PasswordResetRequestForm
    subject_template_name = "emails/password_reset_subject.txt"
    email_template_name = "emails/password_reset.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

    @property
    def extra_email_context(self):
        return {"hours": settings.PASSWORD_RESET_TIMEOUT // 3600}


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Contraseña nueva desde el enlace. El enlace vence con PASSWORD_RESET_TIMEOUT."""

    template_name = "accounts/password_reset_confirm.html"
    form_class = NewPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
