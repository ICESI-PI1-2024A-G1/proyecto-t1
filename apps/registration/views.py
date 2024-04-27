"""
Registration views

This module contains views for handling registration-related operations within the application.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.requests import views
import utils.utils as utils
import re


User = get_user_model()


# Global variable to store the random code
global random_code


def register_view(request):
    """
    View function for user registration.

    Handles user registration by validating user input and sending a verification email.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response or redirection to another view.

    Raises:
        Exception: If there's an error during registration.
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/requests")
        else:
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
            elif not re.compile(r"[^@]+@[^@]+\.[^@]+").match(request.POST["correo"]):
                return render(
                    request,
                    "register.html",
                    {
                        "message": "Por favor, ingrese un correo válido.",
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
                # Save user data in session
                request.session["first_name"] = request.POST["nombre"]
                request.session["last_name"] = request.POST["apellido"]
                request.session["id"] = request.POST["cedula"]
                request.session["email"] = request.POST["correo"]
                request.session["password"] = request.POST["contrasena"]

                # Generate random code
                random_code = utils.generate_random_code()
                request.session["random_code"] = random_code
                # print(random_code)

                # Send verification email
                utils.send_verification_email(
                    request,
                    "Verificación de correo",
                    "Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                    request.POST["correo"],
                    "Hola, bienvenido al Sistema de Contabilidad de la Universidad ICESI.\n\nSu código de verificación es: "
                    + random_code
                    + "\n\nSi no ha solicitado este correo, por favor ignorelo.",
                )

                # Set has_registered session to limit access to the verifyEmail view
                request.session["has_registered"] = True

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
    """
    View function for verifying email during registration.

    Verifies the email using the provided code and creates a new user upon successful verification.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response or redirection to another view.
    """
    if request.method == "GET":
        if request.session.get("has_registered") == True:
            request.session["has_registered"] = False
            return render(request, "verifyEmailReg.html")
        else:
            if request.user.is_authenticated:
                return redirect("/requests")
            else:
                return redirect("login:login_view")
    else:
        if request.POST["verificationCode"] == request.session.get("random_code"):

            id = request.session.get("id")
            username = request.session.get("id")
            first_name = request.session.get("first_name")
            last_name = request.session.get("last_name")
            password = request.session.get("password")
            email = request.session.get("email")

            user = User.objects.create_user(
                id=id,
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()

            messages.success(request, "Usuario registrado correctamente.")
            return redirect("login:login_view")
        else:
            messages.error(request, "Código de verificación incorrecto.")
            return render(request, "verifyEmailReg.html")
