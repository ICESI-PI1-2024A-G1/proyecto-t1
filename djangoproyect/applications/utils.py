from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
import random
import string


def send_verification_email(request, subject, bigSubject, email, message):
    template = render_to_string(
        "email_template.html",
        {
            "message": (message),
        },
    )

    email = EmailMessage(
        subject,
        template,
        bigSubject,
        [email],
    )

    # Email sender
    email.fail_silently = False
    email.send()

    messages.success(request, "Correo enviado exitosamente")


def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))
