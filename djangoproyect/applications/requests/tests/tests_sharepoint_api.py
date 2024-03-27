import os
import unittest
import json
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from api.sharepoint_api import SharePointAPI

EXCEL_FILE_PATH = os.path.join(
    settings.BASE_DIR,
    "static",
    "requests",
    "emulation",
    "requests_test_database.xlsx",
)


class SharePointAPITestCase(TestCase):
    def setUp(self):
        self.sharepoint_api = SharePointAPI(excel_path=EXCEL_FILE_PATH)

    def test_get_request_by_id_existing_id(self):
        response = self.sharepoint_api.get_request_by_id(id=123)
        self.assertEqual(response.status_code, 200)

    def test_get_request_by_id_non_existing_id(self):
        response = self.sharepoint_api.get_request_by_id(id=999)
        self.assertEqual(response.status_code, 404)

    def test_get_all_requests(self):
        response = self.sharepoint_api.get_all_requests()
        self.assertEqual(response.status_code, 200)

    def test_update_data_existing_id(self):
        response = self.sharepoint_api.update_data(
            id=123, new_data={"status": "Completed"}
        )
        self.assertEqual(response.status_code, 200)

    def test_update_data_non_existing_id(self):
        response = self.sharepoint_api.update_data(
            id=999, new_data={"status": "Completed"}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_data_existing_id(self):
        response = self.sharepoint_api.delete_data(id=123)
        self.assertEqual(response.status_code, 200)

    def test_delete_data_non_existing_id(self):
        response = self.sharepoint_api.delete_data(id=999)
        self.assertEqual(response.status_code, 404)

    def test_search_data_existing_query(self):
        response = self.sharepoint_api.search_data(query="Manager")
        self.assertEqual(response.status_code, 200)

    def test_search_data_non_existing_query(self):
        response = self.sharepoint_api.search_data(query="NonExistent")
        self.assertEqual(response.status_code, 200)
