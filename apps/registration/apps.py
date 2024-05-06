"""
Registration app

This module defines the configuration for the "registration" Django app.
"""

from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    """
    Class: RegistrationConfig

    This class represents the configuration for the "registration" Django app.

    Attributes:
        default_auto_field (str): The default primary key field type.
        name (str): The name of the Django app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.registration"
