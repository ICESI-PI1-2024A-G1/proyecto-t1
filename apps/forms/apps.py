from django.apps import AppConfig


class FormsConfig(AppConfig):
    """
    AppConfig class for the forms app.

    This class defines the configuration for the forms app in Django.
    """
    default_auto_field = "django.db.models.BigAutoField"
    """
    The name of the AutoField to use for models that don't specify a primary key field.

    This attribute specifies the type of AutoField that Django should use for
    automatically created primary key fields.
    """
    name = "apps.forms"
    """
    The full Python path to the application, including the package.

    This attribute specifies the full Python import path to the application.
    """