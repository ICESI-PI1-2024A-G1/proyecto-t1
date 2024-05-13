import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from apps.login.backends import IDBackend

class IDBackendTest(unittest.TestCase): # pragma: no cover

    def setUp(self):
        self.factory = RequestFactory()
        self.backend = IDBackend()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_authenticate_with_valid_credentials(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, id=self.user.id, password='testpassword')
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_credentials(self):
        request = self.factory.post('/')
        user = self.backend.authenticate(request, id=self.user.id, password='wrongpassword')
        self.assertIsNone(user)

    def test_get_user_with_valid_id(self):
        user = self.backend.get_user(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_with_invalid_id(self):
        user = self.backend.get_user(9999)
        self.assertIsNone(user)

if __name__ == '__main__': # pragma: no cover
    unittest.main()