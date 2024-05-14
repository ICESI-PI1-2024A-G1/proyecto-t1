from django.shortcuts import render
import utils.utils as utils
from django.contrib.auth import get_user_model


User = get_user_model()


def sendEmail_view(request):
    """
    View function for sending email.

    Handles both GET and POST requests for sending an email.

    GET request:
    - Renders the 'emailContact.html' template with all users.

    POST request:
    - Extracts email, subject, and message from the request.
    - Constructs the full message including sender information.
    - Sends the email using a utility function.
    - Renders the 'emailContact.html' template with all users again.

    Parameters:
    - request: HttpRequest object representing the request.

    Returns:
    - HttpResponse object rendering the 'emailContact.html' template.
    """
    if request.method == "GET":
        return render(request, "emailContact.html", {"users": User.objects.all()})
    else:
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        fullMessage = (
            message
            + "\n\n"
            + "Enviado por: "
            + (request.user.first_name + " " + request.user.last_name)
            .encode("utf-8")
            .decode("utf-8")
            + "\n"
            + ("Correo: " + request.user.email).encode("utf-8").decode("utf-8")
        )
        utils.send_verification_email(
            request, "Mensaje del portal de contabilidad", subject, email, fullMessage
        )
        return render(request, "emailContact.html", {"users": User.objects.all()})#pragma: no cover
