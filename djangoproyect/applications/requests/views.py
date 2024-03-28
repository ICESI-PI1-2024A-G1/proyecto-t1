import json
import os
from django.http import Http404, JsonResponse
from django.shortcuts import render
from api.sharepoint_api import SharePointAPI
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings

EXCEL_FILE_PATH = os.path.join(
    settings.BASE_DIR,
    "static",
    "requests",
    "emulation",
    "requests_database.xlsx",
)

sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)


@csrf_exempt
def change_requests(request, id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "This view only accepts POST requests."}, status=400
        )

    try:
        curr_request = sharepoint_api.get_request_by_id(id)
        if curr_request.status_code == 200:
            new_status = request.POST.get("newStatus")
            curr_request_data = json.loads(curr_request.content)
            curr_request_data["status"] = new_status
            response = sharepoint_api.update_data(id, curr_request_data)
            if response.status_code == 200:
                return JsonResponse(
                    {
                        "message": f"El estado de la solicitud {id} ha sido actualizado correctamente."
                    }
                )
            else:
                raise Http404("No se pudo actualizar la solicitud.")
        else:
            raise Http404(f"No se encontró la solicitud con ID {id} en SharePointAPI.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


def search(request, query):
    try:
        results = sharepoint_api.search_data(query=query)

        if results.status_code == 200:
            return JsonResponse(json.loads(results.content), safe=False)
        else:
            raise Http404("El archivo Excel no está disponible")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


@never_cache
@login_required
def show_requests(request):
    try:
        response = sharepoint_api.get_all_requests()
        if response.status_code == 200:
            requests_data = json.loads(response.content)
            return render(request, "show-requests.html", {"requests": requests_data})
        else:
            raise Http404("No se pudieron cargar las solicitudes.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


@never_cache
@login_required
def detail_request(request, id):
    try:
        detail = sharepoint_api.get_request_by_id(id)
        if detail.status_code == 200:
            return render(
                request, "request-detail.html", {"request": json.loads(detail.content)}
            )
        else:
            raise Http404(f"No se encontró la solicitud con ID {id} en SharePointAPI.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


def show_traceability(request, request_id):
    pass
