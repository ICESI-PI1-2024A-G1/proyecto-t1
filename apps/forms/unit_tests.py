from django.urls import reverse
from utils import *
from django.test import RequestFactory, TestCase, Client

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker
from apps.forms.views import *
fake = Faker()
User = get_user_model()

"""
Forms Test

This module contains test cases for the views related to forms in the application.
"""
class FormTestCase(TestCase):
    """
    Test case class for testing forms views.

    This class contains test cases for various functionalities of the forms views.

    Attributes:
        client (Client): A Django test client instance.
        user (User): A user instance for testing purposes.
        forms (list): A list of forms data for testing purposes.
    """
    def setUp(self):
        # Set up the test environment by creating a test client and a user.
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(
            id="12345",
            username="12345",
            password="12345",
            first_name="testuser",
            last_name="testuser",
            email=fake.email(),
            is_superuser=True
        )
        self.countries = [City.objects.create(name="Bogota", country=Country.objects.create(name="Colombia", code="CO"))]
        self.banks = [Bank.objects.create(name="Banco Ejemplo")]
        self.account_types = [AccountType.objects.create(name="Tipo de Cuenta Ejemplo")]
        self.dependencies = [Dependency.objects.create(name="Dependencia Ejemplo")]
        self.const_centers = [CostCenter.objects.create(name="Centro de Costo Ejemplo")]
        self.client.login(id="12345", password="12345")
        self.travel_advance_valid_data = {
            "requestDate": "2024-05-13",
            "fullName": "John Doe",
            "idNumber": "123456789",
            "dependence": "Department XYZ",
            "costCenter": "Cost Center ABC",
            "destinationCity": "New York",
            "departureDate": "2024-06-01",
            "returnDate": "2024-06-10",
            "travelReason": "Business trip",
            "currency": "USD",
            "airportTransport": 100,
            "localTransport": 50,
            "food": 200,
            "accommodation": 500,
            "exitTaxes": 50,
            "others": 100,
            "total": 1000,
            "signatureStatus": "Yes",
            "bank": "Bank XYZ",
            "accountType": "Checking",
            "accountNumber": "1234567890",
            "observations": "No special observations",
            "signatureInput": "John Doe's signature"
        }

        self.travel_expense_valid_data = {
            "requestDate": "2024-05-13",
            "fullName": "John Doe",
            "idNumber": "123456789",
            "dependence": "Department XYZ",
            "costCenter": "Cost Center ABC",
            "destinationCity": "New York",
            "departureDate": "2024-06-01",
            "returnDate": "2024-06-10",
            "travelReason": "Business trip",
            "total1": 500,
            "total2": 600,
            "total3": 700,
            "advanceTotal1": 200,
            "advanceTotal2": 300,
            "advanceTotal3": 400,
            "employeeBalance1": 300,
            "employeeBalance2": 300,
            "employeeBalance3": 300,
            "icesiBalance1": 0,
            "icesiBalance2": 0,
            "icesiBalance3": 0,
            "signatureStatus": "Yes",
            "bank": "Bank XYZ",
            "accountType": "Checking",
            "accountNumber": "1234567890",
            "observations": "No special observations",
            "signatureInput": "John Doe's signature",
            # Agregar categorías de ejemplo aquí
            "category_0": "Category 1",
            "provider_0": "Provider 1",
            "nit_0": "NIT 1",
            "concept_0": "Concept 1",
            "pesos_0": 200,
            "dollars_0": 100,
            "euros_0": 100,
            "category_1": "Category 2",
            "provider_1": "Provider 2",
            "nit_1": "NIT 2",
            "concept_1": "Concept 2",
            "pesos_1": 300,
            "dollars_1": 150,
            "euros_1": 150,
            "category_2": "Category 3",
            "provider_2": "Provider 3",
            "nit_2": "NIT 3",
            "concept_2": "Concept 3",
            "pesos_2": 400,
            "dollars_2": 200,
            "euros_2": 200,
        }

        self.advance_legalization_valid_data = {
            "requestDate": "2024-05-13",
            "fullName": "John Doe",
            "idNumber": "123456789",
            "dependence": "Department XYZ",
            "costCenter": "Cost Center ABC",
            "purchaseReason": "Business trip expenses",
            "total": 1000,
            "advanceTotal": 500,
            "employeeBalanceValue": 500,
            "icesiBalanceValue": 0,
            "signatureStatus": "Yes",
            "bank": "Bank XYZ",
            "accountType": "Checking",
            "accountNumber": "1234567890",
            "observations": "No special observations",
            "signatureInput": "John Doe's signature",
            # Agregar categorías de ejemplo aquí
            "category_0": "Category 1",
            "provider_0": "Provider 1",
            "pesos_0": 200,
            "concept_0": "Concept 1",
            "category_1": "Category 2",
            "provider_1": "Provider 2",
            "pesos_1": 300,
            "concept_1": "Concept 2",
            "category_2": "Category 3",
            "provider_2": "Provider 3",
            "pesos_2": 400,
            "concept_2": "Concept 3",
        }
        self.billing_account_valid_data = {
            "requestDate": "2024-05-13",
            "fullName": "John Doe",
            "idNumber": "123456789",
            "value": 1000,
            "conceptReason": "Billing for services",
            "retention": 50,
            "taxPayer": "Taxpayer XYZ",
            "resident": "Yes",
            "requestCity": "City ABC",
            "address": "123 Main St",
            "phoneNumber": "555-1234",
            "signatureStatus": "Yes",
            "bank": "Bank XYZ",
            "accountType": "Checking",
            "accountNumber": "1234567890",
            "cexNumber": "CEX123",
            "signatureInput": "John Doe's signature",
        }
        self.requisition_valid_data = {
            "requestDate": "2024-05-13",
            "fullName": "John Doe",
            "idNumber": "123456789",
            "work": "Project ABC",
            "dependence": "Department XYZ",
            "cenco": "CENCO123",
            "idValue": 1000,
            "description": "Materials for project",
            "signatureStatus": "Yes",
            "bank": "Bank XYZ",
            "accountType": "Checking",
            "accountNumber": "1234567890",
            "observations": "No special observations",
            "signatureInput": "John Doe's signature",
        }



    def test_get_next_id(self):
        next_id = get_next_id()
        self.assertEqual(next_id, 1)

    def test_get_cities_with_countries(self):
        cities = get_cities_with_countries()
        self.assertEqual(len(cities), len(self.countries))

    def test_get_bank_data(self):
        banks = get_bank_data()
        self.assertEqual(len(banks), len(self.banks))

    def test_get_account_types(self):
        account_types = get_account_types()
        self.assertEqual(len(account_types), len(self.account_types))

    def test_get_dependence_data(self):
        dependences = get_dependence_data()
        self.assertEqual(len(dependences), len(self.dependencies))

    def test_get_cost_center_data(self):
        cost_centers = get_cost_center_data()
        self.assertEqual(len(cost_centers), len(self.const_centers))

    def test_create_context(self):
        context = create_context()
        self.assertEqual(context["cities"], get_cities_with_countries())
        self.assertEqual(context["banks"], get_bank_data()) 
        self.assertEqual(context["account_types"], get_account_types()) 
        self.assertEqual(context["dependences"], get_dependence_data()) 
        self.assertEqual(context["cost_centers"], get_cost_center_data())   
        self.assertEqual(context["today"], date.today().isoformat())    

    def test_get_travel_advance(self):
        request = self.factory.get(reverse("forms:travel_advance_request"))
        request.user = self.user
        response = advance_legalization(request)
        self.assertEqual(response.status_code, 200)

    def test_post_travel_advance(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse("forms:travel_advance_request"),
            data=self.travel_advance_valid_data,
        )
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = travel_advance_request(request)
        self.assertEqual(response.status_code, 200)
    
    def test_post_travel_expense_legalization(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse("forms:travel_expense_legalization"),
            data=self.travel_expense_valid_data,
        )
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = travel_expense_legalization(request)
        self.assertEqual(response.status_code, 200)

    def test_post_advance_legalization(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse("forms:advance_legalization"),
            data=self.advance_legalization_valid_data,
        )
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = advance_legalization(request)
        self.assertEqual(response.status_code, 200)

    def test_post_billing_account(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse("forms:billing_account"),
            data=self.billing_account_valid_data,
        )
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = billing_account(request)
        self.assertEqual(response.status_code, 200)

    def test_post_requisition(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse("forms:requisition"),
            data=self.requisition_valid_data,
        )
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = requisition(request)
        self.assertEqual(response.status_code, 200)