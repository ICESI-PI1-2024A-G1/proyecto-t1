from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from applications.requests import views
from django.contrib import messages
import applications.utils as utils

# Global variable to store the random code
global random_code

# Create your views here.
def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated and request.GET.get('logout') != 'true':
            return redirect(views.show_requests)
        else:
            if request.GET.get('logout') == 'true':
                logout(request)
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
                    random_code = utils.generate_random_code()
                    request.session['random_code'] = random_code
                    print("Code: " + random_code)

                    # Send verification email
                    # utils.send_verification_email(
                    #     request,
                    #     "Verificación de correo",
                    #     "Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                    #     user.email,
                    #     "Hola, bienvenido al Sistema de Contabilidad de la Universidad ICESI.\n\nSu código de verificación es: " + random_code + "\n\nSi no ha solicitado este correo, por favor ignorelo."
                    # )

                    request.session['has_logged'] = True
                    
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
        if request.session.get('has_logged') == True:
            request.session['has_logged'] = False
            return render(request, "verifyEmailLog.html")
        else:
            if (request.user.is_authenticated):
                return redirect(views.show_requests)
            else:
                return redirect("login:login_view")
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
            return render(request, "verifyEmailLog.html")
