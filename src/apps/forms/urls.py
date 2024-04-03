from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("add-form/", views.show_forms, name="show_forms"),
    path("form-preview/", views.form_preview, name="form-preview"),
    path("load-template/", views.load_excel_template, name="load_template"),
]
