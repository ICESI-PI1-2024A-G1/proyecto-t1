from django.urls import path
from . import views

app_name = 'errorHandler'

urlpatterns = [
    path("404/", views.error_404_view, name='error_404_view'),
]