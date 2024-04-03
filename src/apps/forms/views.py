import math
from django.shortcuts import render

# Create your views here.

from django.conf import settings
from api.sharepoint_api import SharePointAPI
import os
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def show_forms(request):
    return render(request, "show-forms.html")


@csrf_exempt
def add_form(request):
    if request.method == "GET":
        return render(request, "add-form.html")
    elif request.method == "POST":
        fields = request.POST.getlist("fields[]")
        print(fields)


@csrf_exempt
def load_excel_template(request):
    if request.method == "POST":
        template_file = request.FILES["excel_template"]
        sharepoint_api = SharePointAPI(settings.EXCEL_FILE_PATH)
        api_response = sharepoint_api.get_form_render(excel_file=template_file)
        sheet = json.loads(api_response.content)
        return render(request, "excel-preview.html", {"sheet": sheet})


@csrf_exempt
def form_preview(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        form_fields = data.get("form_fields")
        print(form_fields)
        return render(
            request, "dynamic-form.html", {"fields": form_fields, "showSubmit": False}
        )
