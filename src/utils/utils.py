from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
import random
import string

verification_codes = {} 

def send_verification_email(request, subject, bigSubject, email, message, attachment=None):
    """
    Sends a verification email using Django's EmailMessage.

    Parameters:
        request (HttpRequest): The HTTP request object.
        subject (str): The subject of the email.
        bigSubject (str): The "from" field of the email.
        email (str): The recipient's email address.
        message (str): The message body of the email.
        attachment (bytes, optional): The file to attach to the email. Defaults to None.

    Returns:
        None
    """
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
        email if isinstance(email, list) else [email],
    )

    if attachment is not None:
        email.attach('Solicitud.pdf', attachment, 'application/pdf')

    # Email sender
    email.fail_silently = False
    # print(email)
    email.send()

    messages.success(request, "Correo enviado exitosamente")


def generate_random_code(length=6):
    """
    Generates a random alphanumeric code of a specified length.

    Parameters:
        length (int): The length of the generated code. Default is 6.

    Returns:
        str: A random alphanumeric code.
    """
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))
