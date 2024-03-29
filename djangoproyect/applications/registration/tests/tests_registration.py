from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_register_view_get(self):
        response = self.client.get(reverse('registration:register_view'))
        self.assertEqual(response.status_code, 200)  # Should render register.html

    def test_register_view_post_existing_user(self):
        response = self.client.post(reverse('registration:register_view'), {'nombre': 'Test', 'apellido': 'User', 'cedula': '123456', 'correo': 'test@u.icesi.edu.co', 'contrasena': '12345', 'confirmar_contrasena': '12345'})
        self.assertEqual(response.status_code, 200)  # Should render register.html with error message

    def test_register_view_post_invalid_cedula(self):
        response = self.client.post(reverse('registration:register_view'), {'nombre': 'Test', 'apellido': 'User', 'cedula': '123', 'correo': 'test@u.icesi.edu.co', 'contrasena': '12345', 'confirmar_contrasena': '12345'})
        self.assertEqual(response.status_code, 200)  # Should render register.html with error message

    def test_register_view_post_invalid_email(self):
        response = self.client.post(reverse('registration:register_view'), {'nombre': 'Test', 'apellido': 'User', 'cedula': '1234567', 'correo': 'test@gmail.com', 'contrasena': '12345', 'confirmar_contrasena': '12345'})
        self.assertEqual(response.status_code, 200)  # Should render register.html with error message

    def test_register_view_post_invalid_password(self):
        response = self.client.post(reverse('registration:register_view'), {'nombre': 'Test', 'apellido': 'User', 'cedula': '1234567', 'correo': 'test@u.icesi.edu.co', 'contrasena': '123', 'confirmar_contrasena': '123'})
        self.assertEqual(response.status_code, 200)  # Should render register.html with error message

    def test_register_view_post_passwords_do_not_match(self):
        response = self.client.post(reverse('registration:register_view'), {'nombre': 'Test', 'apellido': 'User', 'cedula': '1234567', 'correo': 'test@u.icesi.edu.co', 'contrasena': '12345678', 'confirmar_contrasena': '87654321'})
        self.assertEqual(response.status_code, 200)  # Should render register.html with error message

    def test_register_view_post_valid_user(self):
        response = self.client.post(reverse('registration:register_view'), {'nombre': 'Test', 'apellido': 'User', 'cedula': '1234567', 'correo': 'test@u.icesi.edu.co', 'contrasena': '12345678', 'confirmar_contrasena': '12345678'})
        self.assertEqual(response.status_code, 302)  # Should redirect to verifyEmail_view

class VerifyEmailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['random_code'] = 'ABC123'
        session['id'] = '1234567'
        session['username'] = '1234567'
        session['first_name'] = 'Test'
        session['last_name'] = 'User'
        session['email'] = 'test@u.icesi.edu.co'
        session['password'] = '123456789'
        session['has_registered'] = True
        session.save()

    def test_verify_email_view_get(self):
        response = self.client.get(reverse('registration:verifyEmail_view'))
        self.assertEqual(response.status_code, 200)  # Should render verifyEmail.html

    def test_verify_email_view_post_invalid_code(self):
        response = self.client.post(reverse('registration:verifyEmail_view'), {'verificationCode': '123ABC'})
        self.assertEqual(response.status_code, 200)  # Should render verifyEmail.html with error message

    def test_verify_email_view_post_valid_code(self):
        response = self.client.post(reverse('registration:verifyEmail_view'), {'verificationCode': 'ABC123'})
        print(self.client.session['random_code'])
        self.assertEqual(response.status_code, 302)  # Should redirect to login_view