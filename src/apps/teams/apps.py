"""
Request app

This module defines the configuration for the "teams" Django app.
"""

from django.apps import AppConfig


class TeamsConfig(AppConfig):
    """
    Configuration class for the Teams app.

    Attributes:
        default_auto_field (str): Specifies the default primary key type for models.
        name (str): Specifies the application name ("apps.teams").

    Note:
        This configuration class is used to configure settings for the Teams app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.teams"
