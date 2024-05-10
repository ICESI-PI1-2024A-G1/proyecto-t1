from utils import *
from utils.utils import generate_random_code, send_verification_email
from django.test import TestCase

from django.http import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage

"""
Request Test

This module contains test cases for the views related to requests in the application.
"""
from django.test import TestCase

class UtilsTest(TestCase):
    """
    Test case class for testing request views.

    This class contains test cases for various functionalities of the request views.

    Attributes:
        client (Client): A Django test client instance.
        api (SharePointAPI): An instance of the SharePointAPI class.
        user (User): A user instance for testing purposes.
        requests (list): A list of request data for testing purposes.
    """

    def setUp(self):
        # Configurar la solicitud HTTP falsa para los casos de prueba
        self.request = HttpRequest()
        self.request.session = {}
        self.request._messages = FallbackStorage(self.request)

    def test_generate_random_code_default_length(self):
        # Prueba si el código generado tiene la longitud predeterminada (6)
        random_code = generate_random_code()
        self.assertEqual(len(random_code), 6)

    def test_generate_random_code_custom_length(self):
        # Prueba si el código generado tiene la longitud personalizada
        custom_length = 8
        random_code =  generate_random_code(length=custom_length)
        self.assertEqual(len(random_code), custom_length)

    def test_generate_random_code_alphanumeric(self):
        # Prueba si el código generado es alfanumérico
        random_code =  generate_random_code(length=10)
        self.assertTrue(random_code.isalnum())

    def test_send_verification_email(self):
        subject = "Verification Subject"
        big_subject = "From: sender@example.com"
        email = "recipient@example.com"
        message = "Verification message"
        attachments = [{"name": "attachment.txt", "content": b"Attachment content", "type": "text/plain"}]
        
        send_verification_email(self.request, subject, big_subject, email, message, attachments)
        
        # Verificar si el mensaje de éxito se ha agregado a la sesión
        self.assertEqual(len(self.request._messages), 1)
        success_message = list(self.request._messages)[0]
        self.assertEqual(success_message.tags, "success")
        self.assertEqual(success_message.message, "Correo enviado exitosamente")

    def test_generate_random_code_default_length(self):
            random_code = generate_random_code()
            self.assertEqual(len(random_code), 6)

    def test_generate_random_code_custom_length(self):
        custom_length = 8
        random_code = generate_random_code(length=custom_length)
        self.assertEqual(len(random_code), custom_length)

    def test_generate_random_code_alphanumeric(self):
        random_code = generate_random_code(length=10)
        self.assertTrue(random_code.isalnum())

    def test_generate_random_code_min_length(self):
        random_code = generate_random_code(length=1)
        self.assertEqual(len(random_code), 1)

    def test_generate_random_code_max_length(self):
        random_code = generate_random_code(length=100)
        self.assertLessEqual(len(random_code), 100)

    def test_generate_random_code_data_type(self):
        random_code = generate_random_code(length=8)
        self.assertIsInstance(random_code, str)

    def test_generate_random_code_unique(self):
        codes = set()
        for _ in range(100):
            code = generate_random_code()
            self.assertNotIn(code, codes)
            codes.add(code)

    def test_generate_random_code_special_characters(self):
        random_code = generate_random_code(length=10)
        self.assertTrue(all(char.isalnum() for char in random_code))

    def test_send_verification_email(self):
        subject = "Verification Subject"
        big_subject = "From: sender@example.com"
        email = "recipient@example.com"
        message = "Verification message"
        attachments = [{"name": "attachment.txt", "content": b"Attachment content", "type": "text/plain"}]
        
        send_verification_email(self.request, subject, big_subject, email, message, attachments)
        
        self.assertEqual(len(self.request._messages), 1)
        success_message = list(self.request._messages)[0]
        self.assertEqual(success_message.tags, "success")
        self.assertEqual(success_message.message, "Correo enviado exitosamente")

    def test_send_verification_email_success(self):
        subject = "Verification Subject"
        email = "recipient@example.com"
        message = "Verification message"
        attachments = [{"name": "attachment.txt", "content": b"Attachment content", "type": "text/plain"}]
        
        send_verification_email(self.request, subject, email, message, attachments)
        
        self.assertEqual(len(self.request._messages), 1)
        success_message = list(self.request._messages)[0]
        self.assertEqual(success_message.tags, "success")
        self.assertEqual(success_message.message, "Correo enviado exitosamente")
