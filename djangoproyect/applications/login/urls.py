from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path("", views.login_view, name='login_view'),
    path("verifyEmail/", views.verify_email_view, name='verifyEmail_view')
]
