from django.shortcuts import render
import utils.utils as utils
from django.contrib.auth import get_user_model


User = get_user_model()


def sendEmail_view(request):
    """View function for sending email."""
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
        return render(request, "emailContact.html", {"users": User.objects.all()})
