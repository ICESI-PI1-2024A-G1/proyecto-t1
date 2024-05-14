from utils import *
from django.contrib import admin
from utils.models import CustomUser
from utils.admin import UserAdmin
from utils.forms import CustomUserChangeForm
from django.test import TestCase

class AdminTest(TestCase):
    def setUp(self):
        """
        Set up test data for admin-related tests.
        
        Returns:
            None
        """
        self.user_data = {
            "id": "123456",
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "testpassword",
            "is_superuser": True,
            "is_leader": False,
            "is_member": True,
            "is_applicant": False,
            "is_none": False,
        }

    def test_admin_settings(self):
        """
        Test admin settings for CustomUser model.
        
        Verifies if CustomUser is registered in the admin,
        if UserAdmin is associated with CustomUser in the admin,
        and checks configurations of UserAdmin.
        
        Returns:
            None
        """
 
        self.assertTrue(admin.site.is_registered(CustomUser))

        self.assertIsInstance(admin.site._registry[CustomUser], UserAdmin)

        user_admin = admin.site._registry[CustomUser]
        self.assertEqual(user_admin.list_display, ("first_name", "last_name", "is_superuser", "is_leader", "is_member", "is_applicant", "is_none"))
        self.assertEqual(user_admin.search_fields, ("first_name", "last_name"))
        self.assertEqual(user_admin.list_editable, ("is_superuser", "is_leader", "is_member", "is_applicant", "is_none"))
        self.assertEqual(user_admin.list_filter, ("is_superuser", "is_leader", "is_member", "is_applicant", "is_none"))
        self.assertEqual(user_admin.list_per_page, 10)
        self.assertEqual(user_admin.form, CustomUserChangeForm)


    def test_custom_user_representation(self):
        """
        Test the representation of CustomUser objects.
        
        Creates a CustomUser object and checks its string representation.
        
        Returns:
            None
        """
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(str(user), f"{user.first_name} {user.last_name} (@{user.username})")
        
    def test_admin_create_user(self):
        """
        Test the creation of a user via admin interface.
        
        Creates a UserAdmin instance and verifies its existence.
        
        Returns:
            None
        """
        user_admin = UserAdmin(CustomUser, admin.site)
        self.assertIsNotNone(user_admin)
