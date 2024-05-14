from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from .views import sendEmail_view
from django.contrib.messages.storage.base import BaseStorage
from django.contrib.messages.storage.fallback import FallbackStorage

class SendEmailViewTest(TestCase):
    """
    Test cases for the sendEmail_view function.
    """
    def setUp(self):
        """
        Set up test data.
        """
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_send_email_view_get(self):
        """
        Set up test data.
        """
        request = self.factory.get(reverse('contact:email_contact'))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = sendEmail_view(request)
        self.assertIn('emailContact', response.content.decode())
    def test_send_email_view_post(self):
        """
        Test POST request to the sendEmail_view.
        """
        request = self.factory.post(reverse('contact:email_contact'), data={'email': 'recipient@example.com', 'subject': 'Test Subject', 'message': 'Test Message'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = sendEmail_view(request)
        self.assertIn('Correo enviado exitosamente', response.content.decode())
