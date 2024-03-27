from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from applications.requests import views
from django.contrib import messages
import utils.utils as utils


User = get_user_model()


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
                if user.is_staff or user.is_leader:

                    request.session['user_id'] = user.id
                    
                    # Generate random code
                    random_code = utils.generate_random_code()
                    request.session['random_code'] = random_code
                    print("Code: " + random_code)

                    # Send verification email
                    utils.send_verification_email(
                        request,
                        "Verificación de correo",
                        "Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                        user.email,
                        "Hola, bienvenido al Sistema de Contabilidad de la Universidad ICESI.\n\nSu código de verificación es: " + random_code + "\n\nSi no ha solicitado este correo, por favor ignorelo."
                    )
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
                        "message": "El usuario ingresado no está registrado en la plataforma."
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


# Verification after login
def verify_email_view(request):
    context = {'form_action': 'login:verifyEmail_view'}
    if request.method == "GET":
        if request.session.get('has_logged') == True:
            request.session['has_logged'] = False
            return render(request, "verifyEmailLog.html", context)
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
            return render(request, "verifyEmailLog.html", context)
        
'''
Change password methods

1. reset_password_view: Request id after clicking "Forgot password?"
2. verify_email_reset_view: Verification after putting id in "Forgot password?" to verify identity
3. change_password_view: Change password after verifying identity
4. Return to login_view after changing password
'''

# Request id after clicking "Forgot password?"
def reset_password_view(request):
    if request.method == "GET":
        return render(request, "reset_password.html")
    else:
        id = request.POST["userId"]
        if (User.objects.filter(id=id).exists()):
            request.session['user_id'] = id
            # Generate random code
            random_code = utils.generate_random_code()
            request.session['random_code'] = random_code
            print("Code: " + random_code)
            user = User.objects.get(id=id)
            email = user.email
            # Send verification email
            utils.send_verification_email(
                request,
                "Verificación de correo",
                "Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                email,
                "Hola, se ha solicitado un cambio de contraseña.\n\nSu código de verificación es: " + random_code + "\n\nSi no ha solicitado este cambio, ignore este mensaje."
            )
            request.session['has_requested_password'] = True
            return redirect('login:verify_email_reset_view')
        else:
            messages.error(request, 'Usuario no encontrado.')
            return render(request, "reset_password.html")


# Verification after putting id in "Forgot password?" to verify identity
def verify_email_reset_view(request):
    context = {'form_action': 'login:verify_email_reset_view'}
    if request.method == "GET":
        if request.session.get('has_requested_password') == True:
            request.session['has_requested_password'] = False
            return render(request, "verifyEmailLog.html", context)
        else:
            if request.user.is_authenticated:
                return redirect(views.show_requests)
            else:
                return redirect("login:login_view")
    else:
        if request.POST["verificationCode"] == request.session.get('random_code'):
            return redirect("login:change_password_view")
        else:
            messages.error(request, 'Código de verificación incorrecto.')
            return render(request, "verifyEmailLog.html", context)
        

# Change password after verifying identity       
def change_password_view(request):
    if request.method == "GET":
        return render(request, "change_password.html")
    else:
        password = request.POST["password"]
        confirm_password = request.POST["confirmPassword"]
        if password == confirm_password:
            if len(password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                return render(request, "change_password.html")
            else:
                user = User.objects.get(id=request.session.get('user_id'))
                user.set_password(password)
                user.save()
                messages.success(request, 'Las contraseña fue actualizada correctamente.')
                return redirect("login:login_view")
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, "change_password.html")
