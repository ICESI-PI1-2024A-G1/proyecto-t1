from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345', email='testuser@example.com', is_staff=True)

    def test_authenticate_valid_user(self):
        response = self.client.post(reverse('login:login_view'), {'usuario': '1', 'contrasena': '12345'})
        self.assertEqual(response.status_code, 302)  # Should redirect to verifyEmail_view

    def test_authenticate_invalid_user(self):
        response = self.client.post(reverse('login:login_view'), {'usuario': '9999', 'contrasena': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Should render login.html

    def test_generate_random_code(self):
        response = self.client.post(reverse('login:login_view'), {'usuario': '1', 'contrasena': '12345'})
        self.assertIsNotNone(self.client.session.get('random_code'))  # Random code should be stored in session

    def test_verify_email_valid_code(self):
        self.client.post(reverse('login:login_view'), {'usuario': '1', 'contrasena': '12345'})
        response = self.client.post(reverse('login:verifyEmail_view'), {'verificationCode': self.client.session.get('random_code')})
        self.assertEqual(response.status_code, 302)  # Should redirect to show_requests

    def test_verify_email_invalid_code(self):
        self.client.post(reverse('login:login_view'), {'usuario': '1', 'contrasena': '12345'})
        response = self.client.post(reverse('login:verifyEmail_view'), {'verificationCode': 'wrongcode'})
        self.assertEqual(response.status_code, 200)  # Should render verifyEmail.html

    def test_email_sent_on_verify_email(self):
        self.client.post(reverse('login:login_view'), {'usuario': '1', 'contrasena': '12345'})
        self.client.post(reverse('login:verifyEmail_view'), {'verificationCode': self.client.session.get('random_code')})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Verificación de correo')