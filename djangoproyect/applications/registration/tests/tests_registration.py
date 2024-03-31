"""
Registration api 

This module contains test cases for the Registration class.

Classes:
    RegistrationViewTest(TestCase): Test case class for testing registration views.
    VerifyEmailViewTest(TestCase): Test case class for testing email verification views.

"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationViewTest(TestCase):
    """
    Test case class for testing registration views.

    This class contains test cases for various functionalities of the registration view.

    Attributes:
        client (Client): A Django test client instance.
    """

    def setUp(self):
        """
        Set up the test client before each test method execution.
        """
        self.client = Client()

    def test_register_view_get(self):
        """
        Test the GET request to the register view.

        Checks if the register view renders successfully.
        """
        response = self.client.get(reverse("registration:register_view"))
        self.assertEqual(response.status_code, 200)  # Should render register.html

    def test_register_view_post_existing_user(self):
        """
        Test the POST request to the register view with an existing user.

        Checks if the register view renders with an error message for an existing user.
        """
        response = self.client.post(
            reverse("registration:register_view"),
            {
                "nombre": "Test",
                "apellido": "User",
                "cedula": "123456",
                "correo": "test@u.icesi.edu.co",
                "contrasena": "12345",
                "confirmar_contrasena": "12345",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should render register.html with error message

    def test_register_view_post_invalid_cedula(self):
        """
        Test the POST request to the register view with an invalid cedula.

        Checks if the register view renders with an error message for an invalid cedula.
        """
        response = self.client.post(
            reverse("registration:register_view"),
            {
                "nombre": "Test",
                "apellido": "User",
                "cedula": "123",
                "correo": "test@u.icesi.edu.co",
                "contrasena": "12345",
                "confirmar_contrasena": "12345",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should render register.html with error message

    def test_register_view_post_invalid_email(self):
        """
        Test the POST request to the register view with an invalid email.

        Checks if the register view renders with an error message for an invalid email.
        """
        response = self.client.post(
            reverse("registration:register_view"),
            {
                "nombre": "Test",
                "apellido": "User",
                "cedula": "1234567",
                "correo": "test@gmail.com",
                "contrasena": "12345",
                "confirmar_contrasena": "12345",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should render register.html with error message

    def test_register_view_post_invalid_password(self):
        """
        Test the POST request to the register view with an invalid password.

        Checks if the register view renders with an error message for an invalid password.
        """
        response = self.client.post(
            reverse("registration:register_view"),
            {
                "nombre": "Test",
                "apellido": "User",
                "cedula": "1234567",
                "correo": "test@u.icesi.edu.co",
                "contrasena": "123",
                "confirmar_contrasena": "123",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should render register.html with error message

    def test_register_view_post_passwords_do_not_match(self):
        """
        Test the POST request to the register view with passwords that do not match.

        Checks if the register view renders with an error message for non-matching passwords.
        """
        response = self.client.post(
            reverse("registration:register_view"),
            {
                "nombre": "Test",
                "apellido": "User",
                "cedula": "1234567",
                "correo": "test@u.icesi.edu.co",
                "contrasena": "12345678",
                "confirmar_contrasena": "87654321",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should render register.html with error message

    def test_register_view_post_valid_user(self):
        """
        Test the POST request to the register view with valid user data.

        Checks if the register view redirects to verifyEmail_view for a valid user.
        """
        response = self.client.post(
            reverse("registration:register_view"),
            {
                "nombre": "Test",
                "apellido": "User",
                "cedula": "1234567",
                "correo": "test@u.icesi.edu.co",
                "contrasena": "12345678",
                "confirmar_contrasena": "12345678",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect to verifyEmail_view


class VerifyEmailViewTest(TestCase):
    """
    Test case class for testing email verification views.

    This class contains test cases for various functionalities of the email verification view.

    Methods:
        setUp(self): Set up the test client and session data before each test method execution.
        test_verify_email_view_get(self): Test the GET request to the verifyEmail view.
        test_verify_email_view_post_invalid_code(self): Test the POST request with an invalid verification code.
        test_verify_email_view_post_valid_code(self): Test the POST request with a valid verification code.
    """

    def setUp(self):
        """
        Set up the test client and session data before each test method execution.
        """
        self.client = Client()
        session = self.client.session
        session["random_code"] = "ABC123"
        session["id"] = "1234567"
        session["username"] = "1234567"
        session["first_name"] = "Test"
        session["last_name"] = "User"
        session["email"] = "test@u.icesi.edu.co"
        session["password"] = "123456789"
        session["has_registered"] = True
        session.save()

    def test_verify_email_view_get(self):
        """
        Test the GET request to the verifyEmail view.

        Checks if the verifyEmail view renders successfully.
        """
        response = self.client.get(reverse("registration:verifyEmail_view"))
        self.assertEqual(response.status_code, 200)  # Should render verifyEmail.html

    def test_verify_email_view_post_invalid_code(self):
        """
        Test the POST request to the verifyEmail view with an invalid verification code.

        Checks if the verifyEmail view renders with an error message for an invalid code.
        """
        response = self.client.post(
            reverse("registration:verifyEmail_view"), {"verificationCode": "123ABC"}
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should render verifyEmail.html with error message

    def test_verify_email_view_post_valid_code(self):
        """
        Test the POST request to the verifyEmail view with a valid verification code.

        Checks if the verifyEmail view redirects to login_view for a valid code.
        """
        response = self.client.post(
            reverse("registration:verifyEmail_view"), {"verificationCode": "ABC123"}
        )
        # print(self.client.session['random_code'])
        self.assertEqual(response.status_code, 302)  # Should redirect to login_view
