from utils import *
from utils.models import CustomUserManager, CustomUser
from django.test import TestCase
import unittest

from django.test import TestCase

class TestCustomUser(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for custom user-related tests.
        
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
            "is_member": True,
            "is_leader": False,
            "is_superuser": True,
            "is_applicant": False,
            "is_none": False,
        }
        self.user_data2 = {
            "id": "123456",
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "password": "testpassword",
            "is_member": True,
            "is_leader": False,
            "is_superuser": True,
            "is_applicant": False,
            "is_none": False,
        }

    def test_create_user(self):
        """
        Test creating a new user.
        
        Creates a new user with provided data and checks if it's created successfully.
        
        Returns:
            None
        """
        user = CustomUser.objects.create_user(**self.user_data)

        # Verificar que se haya creado correctamente
        self.assertEqual(user.id, self.user_data["id"])
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_create_user_error(self):
        """
        Test creating a new user with missing email.
        
        Attempts to create a new user with missing email and verifies if it raises ValueError.
        
        Returns:
            None
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(**self.user_data2)

    def test_create_superuser(self):
        """
        Test creating a new superuser.
        
        Creates a new superuser with provided data and checks if it's created successfully.
        
        Returns:
            None
        """
        superuser = CustomUser.objects.create_superuser(**self.user_data)

        self.assertEqual(superuser.id, self.user_data["id"])
        self.assertEqual(superuser.username, self.user_data["username"])
        self.assertEqual(superuser.first_name, self.user_data["first_name"])
        self.assertEqual(superuser.last_name, self.user_data["last_name"])
        self.assertEqual(superuser.email, self.user_data["email"])
        self.assertTrue(superuser.check_password(self.user_data["password"]))
        self.assertTrue(superuser.is_superuser)

    def test_user_attributes(self):
        """
        Test attributes of a user.
        
        Creates a new user and verifies its attributes.
        
        Returns:
            None
        """
        user = CustomUser.objects.create_user(**self.user_data)

        self.assertEqual(user.id, self.user_data["id"])
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.is_superuser)

    def test_change_password(self):
        """
        Test changing user password.
        
        Creates a new user, changes its password, and verifies if the password is changed successfully.
        
        Returns:
            None
        """
        user = CustomUser.objects.create_user(**self.user_data)
        new_password = "newpassword"
        user.set_password(new_password)
        user.save()

        self.assertTrue(user.check_password(new_password))

    def test_user_deletion(self):
        """
        Test deleting a user.
        
        Creates a new user, deletes it, and verifies if it's deleted successfully.
        
        Returns:
            None
        """
        user = CustomUser.objects.create_user(**self.user_data)
        user_id = user.id
        user.delete()

        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    def test_superuser_permissions(self):
        """
        Test permissions of a superuser.
        
        Creates a new superuser and verifies its permissions.
        
        Returns:
            None
        """

        superuser = CustomUser.objects.create_superuser(**self.user_data)

        self.assertTrue(superuser.has_perm("app_name.change_customuser"))
        self.assertTrue(superuser.has_perm("app_name.delete_customuser"))


    def test_get_fullname(self):
        """
        Test the get_fullname method of a user.
        
        Creates a new user and verifies the get_fullname method.
        
        Returns:
            None
        """
        user = CustomUser(**self.user_data)

        self.assertEqual(user.get_fullname(), f"{self.user_data['first_name']} {self.user_data['last_name']}")

    def test_get_short_name(self):
        """
        Test the get_short_name method of a user.
        
        Creates a new user and verifies the get_short_name method.
        
        Returns:
            None
        """
        user = CustomUser(**self.user_data)

        self.assertEqual(user.get_short_name(), self.user_data['first_name'])

    def test_str_representation(self):
        """
        Test the __str__ method of a user.
        
        Creates a new user and verifies its string representation.
        
        Returns:
            None
        """
        user = CustomUser(**self.user_data)

        expected_str = f"{self.user_data['first_name']} {self.user_data['last_name']} (@{self.user_data['username']})"
        self.assertEqual(str(user), expected_str)

    def test_is_staff_property(self):
        """
        Test the is_staff property of a user.
        
        Creates a new user and verifies the is_staff property.
        
        Returns:
            None
        """
        user = CustomUser(**self.user_data)

        self.assertEqual(user.is_staff, self.user_data['is_superuser'])

    def test_has_perm_method(self):
        """
        Test the has_perm method of a user.
        
        Creates a new user and verifies the has_perm method.
        
        Returns:
            None
        """
        user = CustomUser(**self.user_data)

        perm = "some_perm"
        self.assertEqual(user.has_perm(perm), self.user_data['is_superuser'])

    def test_has_module_perms_method(self):
        """
        Test the has_module_perms method of a user.
        
        Creates a new user and verifies the has_module_perms method.
        
        Returns:
            None
        """
        user = CustomUser(**self.user_data)

        # Verificar el método has_module_perms
        app_label = "some_app_label"
        self.assertEqual(user.has_module_perms(app_label), self.user_data['is_superuser'])

if __name__ == "__main__": # pragma: no cover
    unittest.main()