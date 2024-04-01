"""
Request Test

This module contains test cases for the views related to requests in the application.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.requests.models import Traceability
from datetime import timedelta
from django.conf import settings
from api.sharepoint_api import SharePointAPI
from faker import Faker
import random
from django.urls import reverse

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
        self.api = SharePointAPI(settings.EXCEL_FILE_PATH)
        self.api.clear_db()
        self.user = User.objects.create_user(
            id="admin",
            username="admin",
            email="test@example.com",
            first_name="admin",
            password="password",
            is_staff=True,
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

            data = {
                "status": random.choice(status_options),
                "manager": self.user.__str__() if i < 5 else fake.first_name(),
                "team": i,
                "initial_date": initial_date.strftime("%d-%m-%Y"),
                "final_date": final_date.strftime("%d-%m-%Y"),
                "fullname": fake.name(),
                "faculty": fake.company(),
                "document": fake.random_number(digits=10),
                "phone_number": fake.phone_number(),
                "email": fake.email(),
                "CENCO": fake.word(),
                "reason": fake.text(max_nb_chars=100),
                "bank": fake.company(),
                "account_type": random.choice(["Ahorros", "Corriente"]),
                "health_provider": fake.company(),
                "pension_fund": fake.company(),
                "arl": fake.company(),
                "contract_value": fake.random_number(digits=7),
                "is_one_time_payment": random.choice([True, False]),
            }

            self.api.create_data(data)
            data["id"] = i + 1
            self.requests.append(data)

    def test_show_requests_admin(self):
        """
        Test case for displaying requests by an admin user.
        """
        response = self.client.get(reverse("requests:show_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(self.requests, response.context["requests"])

    def test_show_requests_member(self):
        """
        Test case for displaying requests by a non-admin user.
        """
        self.user.is_staff = False
        self.user.save()
        response = self.client.get(reverse("requests:show_requests"))
        user_requests = [
            r for r in self.requests if r["manager"] == self.user.__str__()
        ]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(len(user_requests), len(response.context["requests"]))

    def test_show_request_unauthorized(self):
        """
        Test case for attempting to access requests page without authentication.
        """
        self.client.logout()
        response = self.client.get(reverse("requests:show_requests"))
        self.assertRedirects(response, "/logout/?next=/requests/", 302)
        self.assertTemplateUsed("login:login")

    def test_request_detail(self):
        """
        Test case for displaying details of a request.
        """
        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:request_detail", args=[curr_request["id"]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(response.context["request"]["id"], curr_request["id"])

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
            reverse("requests:request_detail", args=[curr_request["id"]])
        )
        self.assertRedirects(response, "/logout/?next=/requests/1/", 302)
        self.assertTemplateUsed("login:login.html")

    def test_change_status_view(self):
        """
        Test case for accessing the change status view.
        """
        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:change_status", args=[curr_request["id"]])
        )
        self.assertEqual(response.context["request"]["id"], curr_request["id"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("change-status.html")

    def test_change_status_view_unauthorized(self):
        """
        Test case for attempting to access the change status view without authentication.
        """
        curr_request = self.requests[0]
        self.client.logout()
        response = self.client.get(
            reverse("requests:change_status", args=[curr_request["id"]])
        )
        self.assertRedirects(response, "/logout/?next=/requests/change-status/1", 302)
        self.assertTemplateUsed("login:login.html")

    def test_change_status_view_not_found(self):
        """
        Test case for attempting to access the change status view for a non-existing request.
        """
        response = self.client.get(reverse("requests:change_status", args=[999]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_change_status(self):
        """
        Test case for changing the status of a request.
        """
        curr_request = self.requests[0]
        prev_state = curr_request["status"]
        new_status = "Rejected"
        data = {"newStatus": new_status}
        response = self.client.post(
            reverse("requests:change_status", args=[curr_request["id"]]), data
        )
        self.assertEqual(response.status_code, 200)
        updated_traceability = Traceability.objects.get(id=curr_request["id"])
        self.assertEqual(updated_traceability.prev_state, prev_state)
        self.assertEqual(updated_traceability.new_state, new_status)

    def test_change_status_unauthorized(self):
        """
        Test case for attempting to change the status of a request without authentication.
        """
        curr_request = self.requests[0]
        self.client.logout()
        data = {"newStatus": "Approved"}
        response = self.client.post(
            reverse("requests:change_status", args=[curr_request["id"]]), data
        )
        self.assertRedirects(response, "/logout/?next=/requests/change-status/1", 302)
        self.assertTemplateUsed("login:login.html")

    def test_change_status_not_found(self):
        """
        Test case for attempting to change the status of a non-existing request.
        """
        data = {"newStatus": "Approved"}
        response = self.client.post(reverse("requests:change_status", args=[999]), data)
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_assign_request_view(self):
        """
        Test case for accessing the assign request view.
        """
        curr_request = self.requests[0]
        response = self.client.get(reverse("requests:assign_request", args=[curr_request["id"]]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("assign-request.html")
        self.assertEqual(response.context["request"]["id"], curr_request["id"])

    def test_assign_request_view_unauthorized(self):
        """
        Test case for attempting to access the assign request view without authentication.
        """
        self.client.logout()
        response = self.client.get(reverse("requests:assign_request", args=[1]))
        self.assertRedirects(response, "/logout/?next=/requests/assign-request/1", 302)
        self.assertTemplateUsed("login:login.html")

    def test_assign_request_view_not_found(self):
        """
        Test case for attempting to access the assign request view for a non-existing request.
        """
        response = self.client.get(reverse("requests:assign_request", args=[999]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_show_traceability(self):
        """
        Test case for displaying traceability of a request.
        """

        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:show_traceability", args=[curr_request["id"]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("show-traceability.html")

    def test_show_traceability_not_found(self):
        """
        Test case for attempting to display traceability of a non-existing request.
        """
        response = self.client.get(
            reverse("requests:show_traceability", args=[300])
        )
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_show_traceability_unauthorized(self):
        """
        Test case for attempting to display traceability of a request without authentication.
        """
        curr_request = self.requests[0]
        self.client.logout()
        response = self.client.get(
            reverse("requests:show_traceability", args=[curr_request["id"]])
        )
        self.assertRedirects(
            response, f"/logout/?next=/requests/show-traceability/{curr_request["id"]}", 302
        )
        self.assertTemplateUsed("login:login.html")
