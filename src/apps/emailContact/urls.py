from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("", views.sendEmail_view, name="email_contact"),
]
