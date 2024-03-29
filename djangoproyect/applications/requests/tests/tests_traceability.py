from django.test import TestCase
from django.urls import reverse
from applications.requests.models import Traceability


class ShowTraceabilityTestCase(TestCase):
    def setUp(self):
        self.trace = Traceability.objects.create(
            request="TestRequest",
            date="2024-03-28",
            prev_state="PreviousState",
            new_state="NewState",
        )

    def test_show_traceability_view(self):
        url = reverse("show_traceability", args=[self.trace.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show-traceability.html")
        self.assertEqual(response.context["trace"], self.trace)

    def test_show_traceability_view_with_invalid_id(self):
        url = reverse(
            "show_traceability", args=[1000]
        )  # Assume there is no object with ID 1000
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_show_traceability_view_with_invalid_request_id(self):
        # Create a traceability object with a different request_id
        trace_with_different_request = Traceability.objects.create(
            request="DifferentRequest",
            date="2024-03-28",
            prevState="PreviousState",
            newState="NewState",
        )
        url = reverse("show_traceability", args=[trace_with_different_request.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
