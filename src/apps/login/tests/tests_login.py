"""
Request Test

This module contains test cases for the views related to login in the application.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from apps.requests import views as requests_views
from apps.teams import views as teams_views


class LoginTest(TestCase):
    """
    Test case class for testing login views.

    This class contains test cases for various functionalities of the login views.

    Attributes:
        client (Client): A Django test client instance.
        user (User): A user instance for testing purposes.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test client and a user.
        """
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            id="12345", password="12345", email="testuser@example.com", is_staff=True
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
