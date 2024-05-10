from utils import *
from django.contrib import admin
from utils.models import CustomUser
from utils.admin import UserAdmin
from utils.forms import CustomUserChangeForm
from django.test import TestCase

class AdminTest(TestCase):
    def setUp(self):
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
        # Verificar si CustomUser está registrado en el admin
        self.assertTrue(admin.site.is_registered(CustomUser))

        # Verificar si UserAdmin está asociado con CustomUser en el admin
        self.assertIsInstance(admin.site._registry[CustomUser], UserAdmin)

        # Verificar configuraciones de UserAdmin
        user_admin = admin.site._registry[CustomUser]
        self.assertEqual(user_admin.list_display, ("first_name", "last_name", "is_superuser", "is_leader", "is_member", "is_applicant", "is_none"))
        self.assertEqual(user_admin.search_fields, ("first_name", "last_name"))
        self.assertEqual(user_admin.list_editable, ("is_superuser", "is_leader", "is_member", "is_applicant", "is_none"))
        self.assertEqual(user_admin.list_filter, ("is_superuser", "is_leader", "is_member", "is_applicant", "is_none"))
        self.assertEqual(user_admin.list_per_page, 10)
        self.assertEqual(user_admin.form, CustomUserChangeForm)


    def test_custom_user_representation(self):
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(str(user), f"{user.first_name} {user.last_name} (@{user.username})")
        
    def test_admin_create_user(self):
        user_admin = UserAdmin(CustomUser, admin.site)
        self.assertIsNotNone(user_admin)
