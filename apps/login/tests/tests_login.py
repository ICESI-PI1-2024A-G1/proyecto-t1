from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages
from apps.login.views import *
from django.contrib.auth import get_user_model
from django.core import mail
User = get_user_model()


class TestChangePasswordView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            id="12345", password="12345", email="testuser@example.com", is_leader=True
        )

    def test_authenticate_valid_user(self):
        """
        Test authentication of a valid user.

        Ensures that a valid user can log in successfully and is redirected
        to the appropriate page.
        """
        response = self.client.post(
            reverse("login:login_view"), {"usuario": "12345", "contrasena": "12345"}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect to verifyEmail_view

    def test_authenticate_invalid_user(self):
        """
        Test authentication of an invalid user.

        Ensures that an invalid user cannot log in and is shown the login page again.
        """
        response = self.client.post(
            reverse("login:login_view"),
            {"usuario": "9999", "contrasena": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)  # Should render login.html

    def test_generate_random_code(self):
        """
        Test generation of a random code.

        Ensures that a random code is generated and stored in the session after login.
        """
        response = self.client.post(
            reverse("login:login_view"), {"usuario": "12345", "contrasena": "12345"}
        )
        self.assertIsNotNone(
            self.client.session.get("random_code")
        )  # Random code should be stored in session

    def test_verify_email_valid_code(self):
        """
        Test verification of a valid email code.

        Ensures that a valid email verification code redirects the user to the appropriate page.
        """
        self.client.post(
            reverse("login:login_view"), {"usuario": "12345", "contrasena": "12345"}
        )
        response = self.client.post(
            reverse("login:verifyEmail_view"),
            {"verificationCode": self.client.session.get("random_code")},
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to show_requests

    def test_verify_email_invalid_code(self):
        """
        Test verification of an invalid email code.

        Ensures that an invalid email verification code renders the verification page again.
        """
        self.client.post(
            reverse("login:login_view"), {"usuario": "12345", "contrasena": "12345"}
        )
        response = self.client.post(
            reverse("login:verifyEmail_view"), {"verificationCode": "wrongcode"}
        )
        self.assertEqual(response.status_code, 200)  # Should render verifyEmail.html

    def test_email_sent_on_verify_email(self):
        """
        Test email sent on verifying email.

        Ensures that an email is sent when the user verifies their email address.
        """
        self.client.post(
            reverse("login:login_view"), {"usuario": "12345", "contrasena": "12345"}
        )
        self.client.post(
            reverse("login:verifyEmail_view"),
            {"verificationCode": self.client.session.get("random_code")},
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Verificación de correo")

    def test_access_show_requests_without_login(self):
        """
        Test access to show requests page without login.

        Ensures that accessing the show requests page without logging in redirects the user.
        """
        response = self.client.get(reverse("requests:show_requests"))
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect because user is not logged in

    def test_access_show_teams_without_login(self):
        """
        Test access to show teams page without login.

        Ensures that accessing the show teams page without logging in redirects the user.
        """
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect because user is not logged in

    def test_change_password_view(self):
        # Configurar la sesión simulada
        session = self.client.session
        session['has_requested_password'] = True
        session['user_id'] = self.user.id
        session.save()
        data = {'password': 'newpassword', 'confirmPassword': 'newpassword'}
        request = self.factory.post(reverse('login:change_password_view'), data)
        request.session = session
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = change_password_view(request)
        self.assertEqual(response.status_code, 302)

    def test_short_password(self):
        data_short_password = {'password': 'short', 'confirmPassword': 'short'}
        request_short_password = self.factory.post(reverse('login:change_password_view'), data_short_password)
        request_short_password.session = self.client.session
        messages_short_password = FallbackStorage(request_short_password)
        setattr(request_short_password, '_messages', messages_short_password)
        response_short_password = change_password_view(request_short_password)
        self.assertEqual(response_short_password.status_code, 200)  # Verificar que la vista se haya renderizado nuevamente
        self.assertContains(response_short_password, "La contraseña debe tener al menos 8 caracteres.")

    def test_mismatch_passwords(self):
        data_mismatch_passwords = {'password': 'password1', 'confirmPassword': 'password2'}
        request_mismatch_passwords = self.factory.post(reverse('login:change_password_view'), data_mismatch_passwords)
        request_mismatch_passwords.session = self.client.session
        messages_mismatch_passwords = FallbackStorage(request_mismatch_passwords)
        setattr(request_mismatch_passwords, '_messages', messages_mismatch_passwords)
        response_mismatch_passwords = change_password_view(request_mismatch_passwords)
        self.assertEqual(response_mismatch_passwords.status_code, 200)  # Verificar que la vista se haya renderizado nuevamente
        self.assertContains(response_mismatch_passwords, "Las contraseñas no coinciden.")

    def test_get_no_session(self):
        # Configurar la sesión simulada
        self.client.logout()
        session = self.client.session
        session['has_requested_password'] = True
        session['user_id'] = self.user.id
        session.save()
        data = {'password': 'newpassword', 'confirmPassword': 'newpassword'}
        request = self.factory.post(reverse('login:change_password_view'), data)
        request.session = session
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = change_password_view(request)
        self.assertEqual(response.status_code, 302)

    def test_reset_password_post(self):
        data = {'userId': self.user.id}
        request = self.factory.post(reverse('login:reset_password_view'), data)
        request.session = self.client.session
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = reset_password_view(request)
        self.assertEqual(response.status_code, 302)  # Verificar redirección después del envío de correo

        # Verificar que se hayan establecido las variables de sesión
        self.assertTrue(request.session.get('user_id') == str(self.user.id))
        self.assertTrue(request.session.get('random_code') is not None)
        self.assertTrue(request.session.get('has_requested_password'))

    def test_verify_email_reset_get(self):
        request_get = self.factory.get(reverse('login:verify_email_reset_view'))
        session = self.client.session
        session['has_requested_password'] = True
        session.save()
        request_get.session = session
        messages = FallbackStorage(request_get)
        setattr(request_get, '_messages', messages)
        response_get = verify_email_reset_view(request_get)
        self.assertEqual(response_get.status_code, 200)  # Verificar que se renderice la página de verificación

    def test_verify_email_reset_post_correct_code(self):
        session = self.client.session
        session['has_requested_password'] = True
        session['random_code'] = 'test_random_code'  # Simular código de verificación
        session.save()
        request_post_correct = self.factory.post(reverse('login:verify_email_reset_view'), {'verificationCode': 'test_random_code'})
        request_post_correct.session = session
        messages = FallbackStorage(request_post_correct)
        setattr(request_post_correct, '_messages', messages)
        response_post_correct = verify_email_reset_view(request_post_correct)
        self.assertEqual(response_post_correct.status_code, 302)

    def test_verify_email_reset_post_incorrect_code(self):
        session = self.client.session
        session['has_requested_password'] = True
        session['random_code'] = 'test_random_code'  # Simular código de verificación
        session.save()
        request_post_incorrect = self.factory.post(reverse('login:verify_email_reset_view'), {'verificationCode': 'incorrect_code'})
        request_post_incorrect.session = session
        messages = FallbackStorage(request_post_incorrect)
        setattr(request_post_incorrect, '_messages', messages)
        response_post_incorrect = verify_email_reset_view(request_post_incorrect)
        self.assertEqual(response_post_incorrect.status_code, 200)  # Verificar que se renderice la página de verificación con un código incorrecto

    def test_login_view_superuser_authenticated(self):
        self.user.is_superuser = True
        self.user.is_leader = False
        self.user.save()
        request = self.factory.get(reverse('login:login_view'))
        request.user = self.user
        request.session = {'has_logged': True, 'has_requested_password': False}  # Simular sesión
        response = login_view(request)
        self.assertEqual(response.status_code, 302)  # Verificar redirección para superusuario

    def test_login_view_leader_authenticated(self):
        self.user.is_superuser = False
        self.user.is_leader = True
        self.user.save()
        request = self.factory.get(reverse('login:login_view'))
        request.user = self.user
        request.session = {'has_logged': True, 'has_requested_password': False}  # Simular sesión
        response = login_view(request)
        self.assertEqual(response.status_code, 302)  # Verificar redirección para líder

    def test_login_view_regular_authenticated(self):
        self.user.is_applicant = True
        self.user.is_leader = False
        self.user.save()
        request = self.factory.get(reverse('login:login_view'))
        request.user = self.user
        request.session = {'has_logged': True, 'has_requested_password': False}  # Simular sesión
        response = login_view(request)
        self.assertEqual(response.status_code, 302)  # Verificar redirección para usuario regular