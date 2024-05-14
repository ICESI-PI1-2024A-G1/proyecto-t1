from django.urls import path
from . import views

app_name = 'errorHandler'
"""
Application namespace.

This variable defines the namespace for the errorHandler app.
"""

urlpatterns = [
    path("404/", views.error_404_view, name='error_404_view'),
    """
    URL pattern for the 404 error view.

    This pattern matches the path '404/' and maps it to the error_404_view function
    from the views module. It also sets the name attribute for the URL pattern.
    """
]