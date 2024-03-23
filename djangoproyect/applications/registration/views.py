from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import applications.utils as utils
import random
import string

# Global variable to store the random code
global random_code


def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        try:
            user_data = {
                "nombre": request.POST.get("nombre", ""),
                "apellido": request.POST.get("apellido", ""),
                "cedula": request.POST.get("cedula", ""),
                "correo": request.POST.get("correo", ""),
            }
            if (
                User.objects.filter(id=request.POST["cedula"]).exists()
                or User.objects.filter(email=request.POST["correo"]).exists()
            ):
                return render(
                    request,
                    "register.html",
                    {
                        "message": "El usuario ya está registrado.",
                        "user_data": user_data,
                    },
                )
            if (
                int(request.POST["cedula"]) <= 1000000
                or len(request.POST["cedula"]) > 12
            ):
                return render(
                    request,
                    "register.html",
                    {
                        "message": "La cédula ingresada no es válida.",
                        "user_data": user_data,
                    },
                )
            elif not request.POST["correo"].endswith(
                "@u.icesi.edu.co"
            ) and not request.POST["correo"].endswith("@icesi.edu.co"):
                return render(
                    request,
                    "register.html",
                    {
                        "message": "El correo ingresado debe ser institucional de ICESI.",
                        "user_data": user_data,
                    },
                )
            elif len(request.POST["contrasena"]) < 8:
                return render(
                    request,
                    "register.html",
                    {
                        "message": "La contraseña debe tener al menos 8 caracteres.",
                        "user_data": user_data,
                    },
                )
            elif request.POST["contrasena"] != request.POST["confirmar_contrasena"]:
                return render(
                    request,
                    "register.html",
                    {
                        "message": "Las contraseñas no coinciden.",
                        "user_data": user_data,
                    },
                )
            else:
                # Generate random code
                random_code = generate_random_code()
                request.session["random_code"] = random_code

                # Send verification email
                utils.send_verification_email(
                    request,
                    "Verificación de correo",
                    "Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                    request.POST["correo"],
                    "Hola, bienvenido al Sistema de Contabilidad de la Universidad ICESI.\n\nSu código de verificación es: " + random_code + "\n\nSi no ha solicitado este correo, por favor ignorelo."
                    )

                return redirect("registration:verifyEmail_view")
        except Exception as e:
            print(e)
            return render(
                request,
                "register.html",
                {
                    "message": "La cédula ingresada no es válida.",
                    "user_data": user_data,
                },
            )


def verify_email_view(request):
    if request.method == "GET":
        return render(request, "verifyEmail.html")
    else:
        if request.POST["verificationCode"] == request.session.get('random_code'):
            
            id = request.session.get('username')
            username = request.session.get('username')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            password = request.session.get('password')
            email = request.session.get('email')

            user = User.objects.create_user(id=id, username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()

            messages.success(request, "Usuario registrado correctamente.")
            return redirect("login:login_view")
        else:
            messages.error(request, "Código de verificación incorrecto.")
            return render(request, "verifyEmail.html")
