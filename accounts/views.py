from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _

from core.emails import send_templated_email
from core.models import LegalText

from .forms import RegistrationForm
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
