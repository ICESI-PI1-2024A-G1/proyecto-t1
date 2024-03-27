import os
import json
from django.conf import settings
import pandas as pd
from django.test import TestCase
from django.urls import reverse
from api.sharepoint_api import SharePointAPI
from django.http import JsonResponse, Http404

EXCEL_FILE_PATH = os.path.join(
    settings.BASE_DIR,
    "static",
    "requests",
    "emulation",
    "requests_test_database.xlsx",
)


class SharePointAPITestCase(TestCase):
    excel_path = EXCEL_FILE_PATH

    def test_get_request_by_id_success(self):
        api = SharePointAPI(self.excel_path)
        response = api.get_request_by_id(10)
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más comprobaciones según la respuesta esperada

    def test_get_request_by_id_not_found(self):
        api = SharePointAPI(self.excel_path)
        with self.assertRaises(Http404):
            api.get_request_by_id(9999)

    def test_get_request_by_id_file_not_found(self):
        # Cambia la ruta del archivo para simular un archivo no encontrado
        api = SharePointAPI("/ruta/no/existente/requests_test_database.xlsx")
        with self.assertRaises(Http404):
            api.get_request_by_id(2)

    # Repite el mismo proceso para los otros métodos

    def test_get_all_requests_success(self):
        api = SharePointAPI(self.excel_path)
        response = api.get_all_requests()
        self.assertEqual(response.status_code, 200)
        # Agrega más comprobaciones si es necesario

    def test_get_all_requests_file_not_found(self):
        # Simula archivo no encontrado
        api = SharePointAPI("/ruta/no/existente/requests_test_database.xlsx")
        with self.assertRaises(Http404):
            api.get_all_requests()

    def test_create_data_success(self):
        api = SharePointAPI(self.excel_path)
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
        response = api.create_data(data)
        self.assertEqual(response.status_code, 201)
        # Agrega comprobaciones adicionales si es necesario

    def test_create_data_failure(self):
        # Simula un escenario de falla, como un error en la creación de datos
        api = SharePointAPI("/ruta/no/existente/requests_test_database.xlsx")
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
            api.create_data(data)

    def test_update_data_success(self):
        api = SharePointAPI(self.excel_path)
        id_to_update = 2
        new_data = {"status": "updated_status"}
        response = api.update_data(id_to_update, new_data)
        self.assertEqual(response.status_code, 200)
        # Agrega comprobaciones adicionales si es necesario

    def test_update_data_not_found(self):
        api = SharePointAPI(self.excel_path)
        id_to_update = 9999  # Un ID que no existe
        new_data = {"status": "updated_status"}
        with self.assertRaises(Http404):
            api.update_data(id_to_update, new_data)

    def test_delete_data_success(self):
        api = SharePointAPI(self.excel_path)
        api.create_data(
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
        data = api.get_all_requests()
        data = json.loads(data.content)
        id_to_delete = data[len(data) - 1]
        response = api.delete_data(id_to_delete["id"])
        self.assertEqual(response.status_code, 200)
        # Agrega comprobaciones adicionales si es necesario

    def test_delete_data_not_found(self):
        api = SharePointAPI(self.excel_path)
        id_to_delete = 9999  # Un ID que no existe
        with self.assertRaises(Http404):
            api.delete_data(id_to_delete)

    def test_search_data_success(self):
        api = SharePointAPI(self.excel_path)
        query = "test"  # Un término de búsqueda que debería tener resultados
        response = api.search_data(query)
        self.assertEqual(response.status_code, 200)
        # Agrega comprobaciones adicionales si es necesario

    def test_search_data_no_results(self):
        api = SharePointAPI(self.excel_path)
        query = "no_results_for_this_query"  # Un término de búsqueda que no debería tener resultados
        response = api.search_data(query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])
