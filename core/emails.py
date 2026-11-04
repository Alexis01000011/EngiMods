"""Envío de correos (docs/arquitectura.md, sección Correo).

Cada correo tiene dos plantillas en templates/emails/: `<nombre>_subject.txt` y `<nombre>.txt`.
El proveedor sale de EMAIL_BACKEND (EM-008); en desarrollo los correos se imprimen en consola.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_templated_email(template_name, context, to):
    subject = render_to_string(f"emails/{template_name}_subject.txt", context)
    body = render_to_string(f"emails/{template_name}.txt", context)
    # El asunto de un correo no admite saltos de línea.
    send_mail(" ".join(subject.split()), body, None, [to])
