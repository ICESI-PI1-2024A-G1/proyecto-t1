"""
Request app

This module defines the configuration for the "requests" Django app.
"""
from django.apps import AppConfig


class RequestsConfig(AppConfig):
    """
    Class: RequestsConfig

    This class represents the configuration for the "requests" Django app.

    Attributes:
        default_auto_field (str): The default primary key field type.
        name (str): The name of the Django app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.requests"
