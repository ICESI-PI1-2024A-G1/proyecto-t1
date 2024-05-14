from django.urls import path
from . import views

app_name = "contact"
"""
Application namespace.

This variable defines the namespace for the contact app.
"""

urlpatterns = [
    path("", views.sendEmail_view, name="email_contact"),
    """
    URL pattern for the email contact view.

    This pattern matches an empty path and maps it to the sendEmail_view function
    from the views module. It also sets the name attribute for the URL pattern.
    """
]
