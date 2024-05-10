from utils import *
from utils.models import CustomUserManager, CustomUser
from django.test import TestCase
import unittest

from django.test import TestCase

class TestCustomUser(unittest.TestCase):
    def setUp(self):
        # Configurar datos de prueba
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

    def test_create_user(self):
        # Crear un nuevo usuario
        user = CustomUser.objects.create_user(**self.user_data)

        # Verificar que se haya creado correctamente
        self.assertEqual(user.id, self.user_data["id"])
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_create_superuser(self):
        # Crear un nuevo superusuario
        superuser = CustomUser.objects.create_superuser(**self.user_data)

        # Verificar que se haya creado correctamente
        self.assertEqual(superuser.id, self.user_data["id"])
        self.assertEqual(superuser.username, self.user_data["username"])
        self.assertEqual(superuser.first_name, self.user_data["first_name"])
        self.assertEqual(superuser.last_name, self.user_data["last_name"])
        self.assertEqual(superuser.email, self.user_data["email"])
        self.assertTrue(superuser.check_password(self.user_data["password"]))
        self.assertTrue(superuser.is_superuser)

    def test_user_attributes(self):
        # Caso de prueba: Verificar los atributos del usuario
        user = CustomUser.objects.create_user(**self.user_data)

        # Verificar que los atributos del usuario sean correctos
        self.assertEqual(user.id, self.user_data["id"])
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.is_superuser)

    def test_change_password(self):
        # Caso de prueba: Cambiar la contraseña de un usuario
        user = CustomUser.objects.create_user(**self.user_data)
        new_password = "newpassword"
        user.set_password(new_password)
        user.save()

        # Verificar que la contraseña se haya cambiado correctamente
        self.assertTrue(user.check_password(new_password))

    def test_user_deletion(self):
        # Caso de prueba: Eliminar un usuario
        user = CustomUser.objects.create_user(**self.user_data)
        user_id = user.id
        user.delete()

        # Verificar que el usuario se haya eliminado correctamente
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    def test_superuser_permissions(self):
        # Caso de prueba: Verificar los permisos de un superusuario
        superuser = CustomUser.objects.create_superuser(**self.user_data)

        # Verificar que el superusuario tenga permisos adecuados
        self.assertTrue(superuser.has_perm("app_name.change_customuser"))
        self.assertTrue(superuser.has_perm("app_name.delete_customuser"))
        # Agregar más permisos según sea necesario

    def test_get_fullname(self):
        # Crear un nuevo usuario
        user = CustomUser(**self.user_data)

        # Verificar el método get_fullname
        self.assertEqual(user.get_fullname(), f"{self.user_data['first_name']} {self.user_data['last_name']}")

    def test_get_short_name(self):
        # Crear un nuevo usuario
        user = CustomUser(**self.user_data)

        # Verificar el método get_short_name
        self.assertEqual(user.get_short_name(), self.user_data['first_name'])

    def test_str_representation(self):
        # Crear un nuevo usuario
        user = CustomUser(**self.user_data)

        # Verificar el método __str__
        expected_str = f"{self.user_data['first_name']} {self.user_data['last_name']} (@{self.user_data['username']})"
        self.assertEqual(str(user), expected_str)

    def test_is_staff_property(self):
        # Crear un nuevo usuario
        user = CustomUser(**self.user_data)

        # Verificar la propiedad is_staff
        self.assertEqual(user.is_staff, self.user_data['is_superuser'])

    def test_has_perm_method(self):
        # Crear un nuevo usuario
        user = CustomUser(**self.user_data)

        # Verificar el método has_perm
        perm = "some_perm"
        self.assertEqual(user.has_perm(perm), self.user_data['is_superuser'])

    def test_has_module_perms_method(self):
        # Crear un nuevo usuario
        user = CustomUser(**self.user_data)

        # Verificar el método has_module_perms
        app_label = "some_app_label"
        self.assertEqual(user.has_module_perms(app_label), self.user_data['is_superuser'])

if __name__ == "__main__":
    unittest.main()