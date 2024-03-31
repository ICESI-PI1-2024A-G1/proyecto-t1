"""
Permissions app
This module contains the configuration for the Permissions application in Django.
"""
from django.apps import AppConfig


class PermissionsConfig(AppConfig):
    """
    Class: PermissionsConfig

    Configuration class for the Permissions application.

    This class provides configuration for the Permissions application.
    It is used to set specific application metadata.

    Attributes:
        default_auto_field (str): The default auto field type used in the models of this application.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.permissions'
