from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from applications.requests import views


# Create your views here.
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        print(request.POST)

        user = authenticate(
            request,
            username=request.POST["usuario"],
            password=request.POST["contrasena"],
        )

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect(views.show_requests)
            else:
                return render(
                    request,
                    "login.html",
                    {"message": "El usuario ingresado no es un administrador"},
                )
        else:
            return render(
                request,
                "login.html",
                {
                    "message": "El usuario registrado no está registrado en la plataforma"
                },
            )
