"""
Request Test

This module contains test cases for the views related to requests in the application.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.conf import settings
from faker import Faker
import random
from django.urls import reverse
from apps.requests.models import SharePoint

fake = Faker()
User = get_user_model()

settings.EXCEL_FILE_PATH = settings.EXCEL_FILE_PATH_TEST


class RequestViewTest(TestCase):
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
        """
        Set up test data and initialize necessary instances.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            id="admin",
            username="admin",
            email="test@example.com",
            first_name="admin",
            password="password",
            is_superuser=True,
        )
        self.client.login(id="admin", password="password")
        self.requests = []

        for i in range(10):
            status_options = [
                "EN PROCESO",
                "APROBADO - CENCO",
                "RECHAZADO - CENCO",
                "APROBADO - DECANO",
                "RECHAZADO - DECANO",
                "PAGADO - CONTABILIDAD",
                "RECHAZADO - CONTABILIDAD",
                "CERRADO",
            ]
            initial_date = fake.date_between(start_date="-30d", end_date="+4d")
            final_date = initial_date + timedelta(days=random.randint(1, 30))

            documents = [
                "Cuenta de cobro",
                "Legalizacion",
                "Anticipo",
                "Viatico",
                "Factura",
                "Factura CEX",
            ]

            data = {
                "status": random.choice(status_options),
                "manager": self.user.__str__() if i < 5 else fake.first_name(),
                "team": i,
                "initial_date": initial_date.strftime("%Y-%m-%d"),
                "final_date": final_date.strftime("%Y-%m-%d"),
                "fullname": fake.name(),
                "faculty": fake.company(),
                "document": random.choice(documents),
                "phone_number": fake.phone_number(),
                "email": fake.email(),
                "CENCO": fake.word(),
                "bank": fake.company(),
                "account_type": random.choice(["Ahorros", "Corriente"]),
                "health_provider": fake.company(),
                "pension_fund": fake.company(),
                "arl": fake.company(),
                "contract_value": fake.random_number(digits=7),
                "is_one_time_payment": random.choice([True, False]),
            }

            newRequest = SharePoint.objects.create(**data)
            self.requests.append(newRequest)

    def test_show_requests_admin(self):
        """
        Test case for displaying requests by an admin user.
        """
        response = self.client.get(reverse("requests:show_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(self.requests, list(response.context["requests"]))

    def test_show_requests_member(self):
        """
        Test case for displaying requests by a non-admin user.
        """
        self.user.is_superuser = False
        self.user.is_member = True
        self.user.save()
        response = self.client.get(reverse("requests:show_requests"))
        user_requests = [r for r in self.requests if r.manager == self.user.__str__()]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(len(user_requests), len(response.context["requests"]))

    def test_show_request_unauthorized(self):
        """
        Test case for attempting to access requests page without authentication.
        """
        self.client.logout()
        response = self.client.get(reverse("requests:show_requests"))
        self.assertRedirects(response, "/logout/?next=/sharepoint/", 302)
        self.assertTemplateUsed("login:login")

    def test_request_detail(self):
        """
        Test case for displaying details of a request.
        """
        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:request_detail", args=[curr_request.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(response.context["request"].id, curr_request.id)

    def test_request_detail_not_found(self):
        """
        Test case for attempting to access details of a non-existing request.
        """
        response = self.client.get(reverse("requests:request_detail", args=[999]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_request_detail_not_unauthorized(self):
        """
        Test case for attempting to access details of a request without authentication.
        """
        curr_request = self.requests[0]
        self.client.logout()
        response = self.client.get(
            reverse("requests:request_detail", args=[curr_request.id])
        )
        self.assertRedirects(response, "/logout/?next=/sharepoint/1/", 302)
        self.assertTemplateUsed("login:login.html")

    def test_correct_document_values(self):
        """
        Test case to verify that first request has a valid document value.
        """
        documents = [
            "Cuenta de cobro",
            "Legalizacion",
            "Anticipo",
            "Viatico",
            "Factura",
            "Factura CEX",
        ]
        curr_request = self.requests[0]
        result = any(
            curr_request.document.lower() == elemento.lower() for elemento in documents
        )
        self.assertTrue(result)

    def test_correct_all_document_values(self):
        """
        Test case to verify that all requests have a valid document value.
        """
        documents = [
            "Cuenta de cobro",
            "Legalizacion",
            "Anticipo",
            "Viatico",
            "Factura",
            "Factura CEX",
        ]
        for curr_request in self.requests:
            result = any(
                curr_request.document.lower() == elemento.lower()
                for elemento in documents
            )
            self.assertTrue(
                result,
                f"Request '{curr_request}' does not have a valid document value.",
            )
