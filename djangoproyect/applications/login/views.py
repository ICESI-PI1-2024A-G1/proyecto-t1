from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from applications.requests import views


# Create your views here.
def login_view(request):
    if request.method == "GET":
        """
        # Sustituye 'nombre_de_usuario', 'correo@ejemplo.com' y 'contraseña123' con los valores deseados
        nombres = ["Juan", "María", "Luis", "Ana", "Carlos"]
        apellidos = ["González", "López", "Martínez", "Sánchez", "Pérez"]

        # Crear y guardar 5 usuarios
        for i in range(5):
            # Nombre de usuario, correo electrónico y contraseña
            username = f"usuario{i+1}"
            email = f"usuario{i+1}@example.com"
            password = "contraseña123"

            # Crear el usuario con first_name y last_name
            user = User.objects.create_user(
                username, email, password, first_name=nombres[i], last_name=apellidos[i]
            )

            # Establecer is_staff como True
            user.is_staff = True

            # Guardar el usuario
            user.save()
        """

        return render(request, "login.html")
    else:
        print(request.POST)
        
        try:
            user = authenticate(
                request,
                id=request.POST["usuario"],
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
        except:
            return render(
                    request,
                    "login.html",
                    {
                        "message": "Ingrese un usuario válido."
                    },
                )
