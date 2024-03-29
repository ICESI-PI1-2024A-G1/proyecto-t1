from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from applications.requests.models import Requests, Traceability
from datetime import date, timedelta
from django.conf import settings
import os
from api.sharepoint_api import SharePointAPI
from openpyxl import Workbook
from faker import Faker
import random
from django.urls import reverse

fake = Faker()


EXCEL_FILE_PATH = os.path.join(
    settings.BASE_DIR,
    "static",
    "requests",
    "emulation",
    "requests_database.xlsx",
)

sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)

User = get_user_model()


class RequestViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        sharepoint_api.clear_db()
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
                "reason": fake.text(),
                "bank": fake.company(),
                "account_type": random.choice(["Ahorros", "Corriente"]),
                "health_provider": fake.company(),
                "pension_fund": fake.company(),
                "arl": fake.company(),
                "contract_value": fake.random_number(digits=7),
                "is_one_time_payment": random.choice([True, False]),
            }

            sharepoint_api.create_data(data)
            data["id"] = i + 1
            self.requests.append(data)

    def test_show_requests_admin(self):
        response = self.client.get(reverse("requests:show_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(self.requests, response.context["requests"])

    def test_show_requests_member(self):
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
        self.client.logout()
        response = self.client.get(reverse("requests:show_requests"))
        self.assertRedirects(response, "/logout/?next=/requests/", 302)
        self.assertTemplateUsed("login:login")

    def test_request_detail(self):
        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:request_detail", args=[curr_request["id"]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("requests:show_requests.html")
        self.assertEqual(response.context["request"], curr_request)

    def test_request_detail_not_found(self):
        response = self.client.get(reverse("requests:request_detail", args=[999]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_request_detail_not_unauthorized(self):
        curr_request = self.requests[0]
        self.client.logout()
        response = self.client.get(
            reverse("requests:request_detail", args=[curr_request["id"]])
        )
        self.assertRedirects(response, "/logout/?next=/requests/1/", 302)
        self.assertTemplateUsed("login:login.html")

    def test_change_status_view(self):
        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:change_status", args=[curr_request["id"]])
        )
        self.assertEqual(response.context["request"], curr_request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("change-status.html")

    def test_change_status_view_unauthorized(self):
        curr_request = self.requests[0]
        self.client.logout()
        response = self.client.get(
            reverse("requests:change_status", args=[curr_request["id"]])
        )
        self.assertRedirects(response, "/logout/?next=/requests/change-status/1", 302)
        self.assertTemplateUsed("login:login.html")

    def test_change_status_view_not_found(self):
        response = self.client.get(reverse("requests:change_status", args=[999]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_change_status(self):
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
        curr_request = self.requests[0]
        self.client.logout()
        data = {"newStatus": "Approved"}
        response = self.client.post(
            reverse("requests:change_status", args=[curr_request["id"]]), data
        )
        self.assertRedirects(response, "/logout/?next=/requests/change-status/1", 302)
        self.assertTemplateUsed("login:login.html")

    def test_change_status_not_found(self):
        data = {"newStatus": "Approved"}
        response = self.client.post(reverse("requests:change_status", args=[999]), data)
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_assign_request_view(self):
        curr_request = self.requests[0]
        response = self.client.get(reverse("requests:assign_request", args=[curr_request["id"]]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("assign-request.html")
        self.assertEqual(response.context["request"], curr_request)

    def test_assign_request_view_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse("requests:assign_request", args=[1]))
        self.assertRedirects(response, "/logout/?next=/requests/assign-request/1", 302)
        self.assertTemplateUsed("login:login.html")

    def test_assign_request_view_not_found(self):
        response = self.client.get(reverse("requests:assign_request", args=[999]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_show_traceability(self):
        curr_request = self.requests[0]
        response = self.client.get(
            reverse("requests:show_traceability", args=[curr_request["id"]])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("show-traceability.html")

    def test_show_traceability_not_found(self):
        response = self.client.get(
            reverse("requests:show_traceability", args=[300])
        )
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_show_traceability_unauthorized(self):
        curr_request = self.requests[0]
        self.client.logout()
        response = self.client.get(
            reverse("requests:show_traceability", args=[curr_request["id"]])
        )
        self.assertRedirects(
            response, f"/logout/?next=/requests/show-traceability/{curr_request["id"]}", 302
        )
        self.assertTemplateUsed("login:login.html")
