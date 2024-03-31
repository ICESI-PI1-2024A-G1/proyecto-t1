from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.

        Parameters:
            email (str): User's email address.
            password (str): User's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            CustomUser: The created user object.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.

        Parameters:
            email (str): Superuser's email address.
            password (str): Superuser's password.
            **extra_fields: Additional fields for the superuser model.

        Returns:
            CustomUser: The created superuser object.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for your application.
    """

    id = models.CharField(primary_key=True, max_length=10)
    username = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=30, verbose_name="Nombre")
    last_name = models.CharField(max_length=30, verbose_name="Apellido")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False, verbose_name="Miembro")
    is_leader = models.BooleanField(default=False, verbose_name="Lider")
    is_superuser = models.BooleanField(default=False, verbose_name="Super Usuario")

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "email",
        "password",
        "is_staff",
        "is_leader",
    ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user_mod"

    def get_full_name(self):
        """
        Returns the user's full name.

        Returns:
            str: The user's full name.
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """
        Returns the user's first name.

        Returns:
            str: The user's first name.
        """
        return self.first_name

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: String representation of the user.
        """
        return f"{self.first_name} {self.last_name} (@{self.username})"
