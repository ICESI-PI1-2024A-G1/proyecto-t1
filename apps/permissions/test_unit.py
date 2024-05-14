import unittest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.permissions.model.filter_logic import SearchFilter
import json
User = get_user_model()

class TestSearchFilter(unittest.TestCase): #pragma: no cover
    def setUp(self):
        User.objects.all().delete()
        self.filter = SearchFilter()
        self.factory = RequestFactory()

    def test_filter_users(self):
        # Create some dummy users for testing
        user1 = User.objects.create(id=1, username='user1', first_name='John', last_name='Doe', email='john@example.com')
        user2 = User.objects.create(id=2, username='user2', first_name='Jane', last_name='Doe', email='jane@example.com')
        
    # Test filtering by last name
        response = self.filter.filter_users('Doe')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        # Test filtering by first name
        response = self.filter.filter_users('Jane')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data[0]['first_name'], 'Jane')

        # Test filtering by user ID (assuming user1 has ID 1 and user2 has ID 2)
        response = self.filter.filter_users(1)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data[0]['id'], "1")

        # Test filtering with a non-existent query
        response = self.filter.filter_users('NonExistentQuery')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode('utf-8'))

    

    def tearDown(self):
        # Clean up created users after tests
        User.objects.all().delete()

if __name__ == '__main__':#pragma: no cover
    unittest.main()
