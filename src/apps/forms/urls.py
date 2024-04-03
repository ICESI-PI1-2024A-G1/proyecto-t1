from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("", views.show_forms, name="show_forms"),
    path("<int:id>/", views.form_details, name="form_details"),
    path("add-form/", views.add_form, name="add_form"),
    path("form-preview/", views.form_preview, name="form-preview"),
    path("load-template/", views.load_excel_template, name="load_template"),
]
