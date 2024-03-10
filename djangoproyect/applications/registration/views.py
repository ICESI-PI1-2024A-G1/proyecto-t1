from django.shortcuts import render, redirect
from applications.login import views
from django.contrib.auth.models import User
from django.contrib import messages

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
                messages.success(request, 'Usuario registrado correctamente.')
                return redirect('login:login_view')
        except:
            return render(
                request,
                "register.html",
                {"message": "La cédula ingresada no es válida.", "user_data": user_data},
            )