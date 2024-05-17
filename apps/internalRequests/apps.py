from django.apps import AppConfig


class InternalrequestsConfig(AppConfig):
    """
    AppConfig class for the 'internalRequests' app.

    Attributes:
        default_auto_field (str): The name of the default auto field to use for models in this app.
        name (str): The full Python path to the application, e.g., 'apps.internalRequests'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.internalRequests'
