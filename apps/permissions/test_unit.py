import unittest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.permissions.model.filter_logic import SearchFilter
import json
User = get_user_model()

class TestSearchFilter(unittest.TestCase): #pragma: no cover
    """
    Test case for the SearchFilter class.
    """
    def setUp(self):
        """
        Set up method to initialize the test environment.
        """
        User.objects.all().delete()
        self.filter = SearchFilter()
        self.factory = RequestFactory()

    def test_filter_users(self):
        """
        Test the filter_users method of the SearchFilter class.
        """
        user1 = User.objects.create(id=1, username='user1', first_name='John', last_name='Doe', email='john@example.com')
        user2 = User.objects.create(id=2, username='user2', first_name='Jane', last_name='Doe', email='jane@example.com')
        
        response = self.filter.filter_users('Doe')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))

        response = self.filter.filter_users('Jane')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data[0]['first_name'], 'Jane')


        response = self.filter.filter_users(1)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data[0]['id'], "1")

        response = self.filter.filter_users('NonExistentQuery')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))

    

    def tearDown(self):
        """
        Clean up method after the tests.
        """
        User.objects.all().delete()

if __name__ == '__main__':#pragma: no cover
    unittest.main()
