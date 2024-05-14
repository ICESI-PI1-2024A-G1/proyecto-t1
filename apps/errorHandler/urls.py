from django.urls import path
from . import views

app_name = 'errorHandler'
"""
Application namespace.

This variable defines the namespace for the errorHandler app.
"""

urlpatterns = [
    path("404/", views.error_404_view, name='error_404_view')
]