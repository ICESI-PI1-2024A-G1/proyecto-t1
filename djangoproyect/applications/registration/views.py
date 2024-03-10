from django.shortcuts import render, redirect
from applications.login import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model

def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        try:
            user_data = {
                "nombre": request.POST.get("nombre", ""),
                "apellido": request.POST.get("apellido", ""),
                "cedula": request.POST.get("cedula", ""),
                "correo": request.POST.get("correo", "")
            }
            if User.objects.filter(id=request.POST["cedula"]).exists():
                return render(
                    request,
                    "register.html",
                    {"message": "El usuario ya está registrado.", "user_data": user_data},
                )
            if int(request.POST["cedula"]) <= 1000000 or len(request.POST["cedula"]) > 12:
                return render(
                    request,
                    "register.html",
                    {"message": "La cédula ingresada no es válida.", "user_data": user_data},
                )
            elif not request.POST["correo"].endswith("@u.icesi.edu.co") and not request.POST["correo"].endswith("@icesi.edu.co"):
                return render(
                    request,
                    "register.html",
                    {"message": "El correo ingresado debe ser institucional de ICESI.", "user_data": user_data},
                )
            elif len(request.POST["contrasena"]) < 8:
                return render(
                    request,
                    "register.html",
                    {"message": "La contraseña debe tener al menos 8 caracteres.", "user_data": user_data},
                )
            elif request.POST["contrasena"] != request.POST["confirmar_contrasena"]:
                return render(
                    request,
                    "register.html",
                    {"message": "Las contraseñas no coinciden.", "user_data": user_data},
                )
            else:
                user = User.objects.create_user(
                id=request.POST["cedula"],
                username=request.POST["cedula"],
                first_name=request.POST["nombre"],
                last_name=request.POST["apellido"],
                password=request.POST["contrasena"],
                email=request.POST["correo"],
                )
                user.save()
                messages.success(request, 'Usuario registrado correctamente.')
                return redirect('login:login_view')
        except Exception as e:
            print(e)
            return render(
                request,
                "register.html",
                {"message": "La cédula ingresada no es válida.", "user_data": user_data},
            )