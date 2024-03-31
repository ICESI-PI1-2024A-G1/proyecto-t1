"""
Sharepoint api 

This module contains test cases for the SharePointAPI class.
"""

from datetime import timedelta
import json
from django.conf import settings
from django.test import TestCase
from api.sharepoint_api import SharePointAPI
from django.http import Http404
from faker import Faker
import random

settings.EXCEL_FILE_PATH = settings.EXCEL_FILE_PATH_TEST

fake = Faker()


class SharePointAPITestCase(TestCase):
    """
    Test case class for testing the SharePointAPI class.

    This class contains test cases for various functionalities of the SharePointAPI class
    to assure a robust functionality whenever it retrieves the data.

    Attributes:
        excel_path (str): The path to the Excel file used for testing.
        api (SharePointAPI): An instance of the SharePointAPI class.
    """

    def setUp(self):
        """
        Set up test data and initialize the SharePointAPI instance.
        """
        self.excel_path = settings.EXCEL_FILE_PATH
        self.api = SharePointAPI(settings.EXCEL_FILE_PATH)
        self.api.clear_db()
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
                "manager": fake.first_name(),
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

    def test_get_request_by_id_success(self):
        """
        Test case for successfully retrieving a request by ID.
        """
        response = self.api.get_request_by_id(10)
        self.assertEqual(response.status_code, 200)

    def test_get_request_by_id_not_found(self):
        """
        Test case for attempting to retrieve a request by an invalid ID.
        """
        with self.assertRaises(Http404):
            self.api.get_request_by_id(9999)

    def test_get_request_by_id_file_not_found(self):
        """
        Test case for attempting to retrieve a request by ID when the file is not found.
        """
        self.api = SharePointAPI("/ruta/no/existente/requests_test_database.xlsx")
        with self.assertRaises(Http404):
            self.api.get_request_by_id(2)

    def test_get_all_requests_success(self):
        """
        Test case for successfully retrieving all requests.
        """
        response = self.api.get_all_requests()
        self.assertEqual(response.status_code, 200)

    def test_get_all_requests_file_not_found(self):
        """
        Test case for attempting to retrieve all requests when the file is not found.
        """
        self.api = SharePointAPI("/ruta/no/existente/requests_test_database.xlsx")
        with self.assertRaises(Http404):
            self.api.get_all_requests()

    def test_create_data_success(self):
        """
        Test case for successfully creating new request data.
        """
        data = {
            "document": "test_document",
            "applicant": "test_applicant",
            "manager": "test_manager",
            "initial_date": "2024-03-27",
            "final_date": "2024-03-28",
            "past_days": 1,
            "description": "test_description",
            "title": "test_title",
            "status": "test_status",
            "req_type": "test_req_type",
            "assigned_users": ["user1", "user2"],
        }
        response = self.api.create_data(data)
        self.assertEqual(response.status_code, 201)

    def test_create_data_failure(self):
        """
        Test case for attempting to create new request data when the file is not found.
        """
        self.api = SharePointAPI("/ruta/no/existente/requests_test_database.xlsx")
        data = {
            "document": "test_document",
            "applicant": "test_applicant",
            "manager": "test_manager",
            "initial_date": "2024-03-27",
            "final_date": "2024-03-28",
            "past_days": 1,
            "description": "test_description",
            "title": "test_title",
            "status": "test_status",
            "req_type": "test_req_type",
            "assigned_users": ["user1", "user2"],
        }
        with self.assertRaises(Http404):
            self.api.create_data(data)

    def test_update_data_success(self):
        """
        Test case for successfully updating request data.
        """
        id_to_update = 2
        new_data = {"status": "updated_status"}
        response = self.api.update_data(id_to_update, new_data)
        self.assertEqual(response.status_code, 200)

    def test_update_data_not_found(self):
        """
        Test case for attempting to update request data with an invalid ID.
        """
        id_to_update = 9999
        new_data = {"status": "updated_status"}
        with self.assertRaises(Http404):
            self.api.update_data(id_to_update, new_data)

    def test_delete_data_success(self):
        """
        Test case for successfully deleting request data.
        """
        self.api.create_data(
            {
                "document": "test_document",
                "applicant": "test_applicant",
                "manager": "test_manager",
                "initial_date": "2024-03-27",
                "final_date": "2024-03-28",
                "past_days": 1,
                "description": "test_description",
                "title": "test_title",
                "status": "test_status",
                "req_type": "test_req_type",
                "assigned_users": ["user1", "user2"],
            }
        )
        data = self.api.get_all_requests()
        data = json.loads(data.content)
        id_to_delete = data[len(data) - 1]
        response = self.api.delete_data(id_to_delete["id"])
        self.assertEqual(response.status_code, 200)

    def test_delete_data_not_found(self):
        """
        Test case for attempting to delete request data with an invalid ID.
        """
        id_to_delete = 9999
        with self.assertRaises(Http404):
            self.api.delete_data(id_to_delete)

    def test_search_data_success(self):
        """
        Test case for successfully searching request data.
        """
        query = "test"
        response = self.api.search_data(query)
        self.assertEqual(response.status_code, 200)

    def test_search_data_no_results(self):
        """
        Test case for searching request data with no results.
        """
        query = "no_results_for_this_query"
        response = self.api.search_data(query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])
