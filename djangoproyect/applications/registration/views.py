from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from email.mime.image import MIMEImage
import random
import string

# Global variable to store the random code
global random_code

def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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
            if User.objects.filter(id=request.POST["cedula"]).exists() or User.objects.filter(email=request.POST["correo"]).exists():
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
                # Obtain the user data
                id = request.POST["cedula"]
                username = request.POST["cedula"]
                first_name = request.POST["nombre"]
                last_name = request.POST["apellido"]
                password = request.POST["contrasena"]
                email = request.POST["correo"]
                
                request.session['id'] = id
                request.session['username'] = username
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['password'] = password
                request.session['email'] = email

                # Generate random code
                random_code = generate_random_code()
                request.session['random_code'] = random_code
                
                # Create the email template
                template = render_to_string(
                    'email_template.html', 
                    {
                        'message': (
                            'Hola, bienvenido al Sistema de Contabilidad de la Universidad ICESI.'
                            '\n\nSu código de verificación es: ' + random_code +
                            '\n\nSi no ha solicitado este correo, por favor ignorelo.'
                        ),
                    }
                )
                
                email = EmailMessage(
                    'Verificación de correo',
                    template,
                    'Verificación de Registro Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>',
                    [email],
                )
                
                # Email sender
                email.fail_silently = False
                email.send()
                
                messages.success(request, 'Correo enviado exitosamente')
                
                return redirect('registration:verifyEmail_view')
        except Exception as e:
            print(e)
            return render(
                request,
                "register.html",
                {"message": "La cédula ingresada no es válida.", "user_data": user_data},
            )
    
def verify_email_view(request):
    if request.method == "GET":
        return render(request, "verifyEmail.html")
    else:
        if request.POST["verificationCode"] == request.session.get('random_code'):
            
            id = request.session.get('id')
            username = request.session.get('username')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            password = request.session.get('password')
            email = request.session.get('email')

            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect("login:login_view")
        else:
            messages.error(request, 'Código de verificación incorrecto.')
            return render(request, "verifyEmail.html")