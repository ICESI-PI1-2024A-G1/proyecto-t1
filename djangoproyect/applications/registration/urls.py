from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path("", views.register_view, name='register_view'),
]