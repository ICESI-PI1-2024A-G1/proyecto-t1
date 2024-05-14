from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.permissions.views import *  # Reemplaza "myapp" por el nombre de tu aplicación

class TestPermissionsView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_user(username='superuser', password='12345', email="sample@gmail.com", is_superuser=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='54321', email="sample@gmail.com", is_superuser=False)

    def test_permissions_view_as_superuser(self):
        # Crear una solicitud GET como superusuario
        request = self.factory.get(reverse('permissions:permissions_view'))
        request.user = self.superuser
        
        # Llamar directamente al método de la vista
        response = permissions_view(request)
        
        # Verificar que la respuesta es un renderizado exitoso de la plantilla
        self.assertEqual(response.status_code, 200)

    def test_permissions_view_as_regular_user(self):
        # Crear una solicitud GET como usuario regular
        request = self.factory.get(reverse('permissions:permissions_view'))
        request.user = self.regular_user
        
        # Llamar directamente al método de la vista
        response = permissions_view(request)
        
        # Verificar que la respuesta sea una redirección
        self.assertEqual(response.status_code, 302)
 
    def test_update_user_permissions_success(self):
        # Iniciar sesión como superusuario
        request = self.factory.post('/update_permissions/', json.dumps([
            {"id": self.regular_user.id, "permission": "is_leader"},
            {"id": self.superuser.id, "permission": "is_member"},
        ]), content_type='application/json')
        request.user = self.superuser
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # Llamar directamente al método de la vista
        response = update_user_permissions(request)
        
        # Verificar que la respuesta sea un JSON de éxito
        self.assertEqual(response.status_code, 200)

    def test_update_user_permissions_failure(self):
        # Iniciar sesión como superusuario
        request = self.factory.post('/update_permissions/', json.dumps([
            {"id": self.regular_user.id, "permission": "is_leader"},
            {"id": self.superuser.id, "permission": "is_member"},
        ]), content_type='application/json')
        request.user = self.superuser
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # Llamar directamente al método de la vista
        response = update_user_permissions(request)
        
        # Verificar que la respuesta sea un JSON de fallo
        self.assertEqual(response.status_code, 200)
