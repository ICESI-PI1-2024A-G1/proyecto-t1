from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from .views import sendEmail_view
from django.contrib.messages.storage.base import BaseStorage
class SendEmailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_send_email_view_get(self):
        request = self.factory.get(reverse('contact:email_contact'))
        request.user = self.user
        response = sendEmail_view(request)
        # Verificar que la respuesta contiene el texto de la plantilla esperado
        self.assertIn('emailContact', response.content.decode())
    def test_send_email_view_post(self):
            request = self.factory.post(reverse('contact:email_contact'), data={'email': 'recipient@example.com', 'subject': 'Test Subject', 'message': 'Test Message'})
            request.user = self.user
            response = sendEmail_view(request)
            # Verificar que la respuesta contiene el texto esperado
            self.assertIn('Correo enviado exitosamente', response.content.decode())