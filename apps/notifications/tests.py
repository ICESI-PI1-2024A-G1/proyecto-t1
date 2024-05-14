from django.urls import reverse
from utils import *
from django.test import RequestFactory, TestCase, Client

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker
from apps.notifications.views import *
fake = Faker()
User = get_user_model()
from datetime import datetime

"""
Forms Test

This module contains test cases for the views related to notifications in the application.
"""
class FormTestCase(TestCase):
    """
    Test case class for testing notifications views.

    This class contains test cases for various functionalities of the notifications views.

    Attributes:
        client (Client): A Django test client instance.
        user (User): A user instance for testing purposes.
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
        StatusNotification.objects.create(
            user_target = self.user,
            modified_by = self.user,
            request_id = 1,
            date = datetime.now(),
            prev_state = "PENDIENTE",
            new_state = "POR APROBAR",
        )
        self.client.login(id="12345", password="12345")

    def test_show_notifications_superuser(self):
        request = self.factory.get(reverse("notifications:show_notifications"))
        request.user = self.user
        response = show_notifications(request)
        self.assertEqual(response.status_code, 200)
    
    def test_show_notifications_leader(self):
        self.user.is_superuser = False
        self.user.is_leader = True
        self.user.save()
        request = self.factory.get(reverse("notifications:show_notifications"))
        request.user = self.user
        response = show_notifications(request)
        self.assertEqual(response.status_code, 200)