from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Token del enlace para verificar el correo (EM-030).

    Vence con PASSWORD_RESET_TIMEOUT de Django (3 días si no se cambia) y deja de servir si
    cambia el correo de la cuenta. Abrirlo otra vez después de verificar no cambia nada.
    Usa su propia sal: un token de recuperación de contraseña no verifica un correo.
    """

    key_salt = "accounts.tokens.EmailVerificationTokenGenerator"

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.email}{timestamp}"


email_verification_token = EmailVerificationTokenGenerator()
