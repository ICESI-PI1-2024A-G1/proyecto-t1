from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
import random
import string

verification_codes = {}


def send_verification_email(
    request, subject, bigSubject, email, message, attachments=None
):
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
    template = render_to_string( # pragma: no cover 
        "email_template.html",
        {
            "message": (message),
        },
    )

    email = EmailMessage(# pragma: no cover 
        subject,
        template,
        bigSubject,
        email if isinstance(email, list) else [email],
    )

    if attachments:# pragma: no cover   
        for attachment in attachments:
            email.attach(attachment["name"], attachment["content"], attachment["type"])

    # Email sender
    email.fail_silently = False# pragma: no cover 
    # print(email)
    email.send() # pragma: no cover 

    messages.success(request, "Correo enviado exitosamente") # pragma: no cover 


def generate_random_code(length=6):
    """
    Generates a random alphanumeric code of a specified length.

    Parameters:
        length (int): The length of the generated code. Default is 6.

    Returns:
        str: A random alphanumeric code.
    """ 
    characters = string.ascii_uppercase + string.digits # pragma: no cover 
    return "".join(random.choice(characters) for _ in range(length))# pragma: no cover 
