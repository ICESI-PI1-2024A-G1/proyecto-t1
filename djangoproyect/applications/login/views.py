from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from applications.requests import views
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
import applications.utils as utils
import random
import string

# Global variable to store the random code
global random_code

def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Create your views here.
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        try:
            user = authenticate(
                request,
                id=request.POST["usuario"],
                password=request.POST["contrasena"],
            )

            if user is not None:
                if user.is_staff:

                    request.session['user_id'] = user.id
                    
                    # Generate random code
                    random_code = generate_random_code()
                    request.session['random_code'] = random_code

                    # Create the email template
                    utils.send_verification_email(
                        request,
                        "Verificación de correo",
                        "Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                        user.email,
                        "Hola, bienvenido al Sistema de Contabilidad de la Universidad ICESI.\n\nSu código de verificación es: " + random_code + "\n\nSi no ha solicitado este correo, por favor ignorelo."
                    )
                    
                    return redirect('login:verifyEmail_view')
                else:
                    return render(
                        request,
                        "login.html",
                        {"message": "El usuario ingresado no es un administrador."},
                    )
            else:
                return render(
                    request,
                    "login.html",
                    {
                        "message": "El usuario registrado no está registrado en la plataforma."
                    },
                )
        except Exception as e:
            print(e)
            return render(
                    request,
                    "login.html",
                    {
                        "message": "Ingrese un usuario válido."
                    },
                )

def verify_email_view(request):
    if request.method == "GET":
        return render(request, "verifyEmail.html")
    else:
        if request.POST["verificationCode"] == request.session.get('random_code'):
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            login(request, user)
            return redirect(views.show_requests)
        else:
            messages.error(request, 'Código de verificación incorrecto.')
            return render(request, "verifyEmail.html")
