from django.shortcuts import render, redirect
from applications.login import views
from django.contrib.auth.models import User

def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        if User.objects.filter(id=request.POST["cedula"]).exists():
            return render(
                request,
                "register.html",
                {"message": "El usuario ya está registrado"},
            )
        elif request.POST["contrasena"] != request.POST["confirmar_contrasena"]:
            return render(
                request,
                "register.html",
                {"message": "Las contraseñas no coinciden"},
            )
        else:
            return redirect(views.login_view)