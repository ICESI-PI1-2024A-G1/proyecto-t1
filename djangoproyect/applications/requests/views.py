import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from applications.requests.model.filter_logic import SearchFilter
from api.sharepoint_api import SharePointAPI
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_FILE_PATH = os.path.join(
    BASE_DIR, "static/requests/emulation/requests_database.xlsx"
)

sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)


@csrf_exempt
def change_requests(request, id):
    if request.method == "POST":
        # Obtener la solicitud por su ID desde SharePointAPI
        solicitud = sharepoint_api.get_request_by_id(id)

        if solicitud:
            # Obtener el nuevo estado de los datos POST
            nuevo_estado = request.POST.get("newStatus")

            # Actualizar el estado de la solicitud en SharePointAPI
            sharepoint_api.update_request_status(id, nuevo_estado)

            # Devolver una respuesta exitosa
            return JsonResponse(
                {
                    "message": f"El estado de la solicitud {id} ha sido actualizado correctamente."
                }
            )
        else:
            return JsonResponse(
                {"error": f"No se encontró la solicitud con ID {id} en SharePointAPI."},
                status=404,
            )
    else:
        # Si la solicitud no es POST, devolver un error
        return JsonResponse(
            {"error": "Esta vista solo acepta solicitudes POST."}, status=400
        )


def search(request, query):
    # Realizar la búsqueda utilizando SharePointAPI
    filtered_requests = sharepoint_api.search_request(query)

    return JsonResponse(filtered_requests)


def show_requests(request):
    # Obtener todas las solicitudes desde SharePointAPI
    requests = sharepoint_api.get_all_requests(request=request)

    return render(request, "show-requests.html", {"requests": requests})


def detail_request(request, id):
    # Obtener los detalles de una solicitud por su ID desde SharePointAPI
    detail = sharepoint_api.get_request_by_id(id)

    if detail:
        return render(request, "request-detail.html", {"request": detail})
    else:
        return JsonResponse(
            {"error": f"No se encontró la solicitud con ID {id} en SharePointAPI."},
            status=404,
        )
