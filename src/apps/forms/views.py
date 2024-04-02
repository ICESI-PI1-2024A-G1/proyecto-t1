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
    if request.method == "GET":
        sharepoint_api = SharePointAPI(os.path.join(settings.EXCEL_FORMS_PATH))
        api_response = sharepoint_api.get_form_render("sample.xlsx")
        sheet = json.loads(api_response.content)
        return render(request, "show-forms.html", {"sheet": sheet})
    elif request.method == "POST":
        fields = request.POST.getlist("fields[]")
        print(fields)


@csrf_exempt
def form_preview(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        form_fields = data.get("form_fields")
        print(form_fields)
        return render(
            request, "dynamic-form.html", {"fields": form_fields, "showSubmit": False}
        )
