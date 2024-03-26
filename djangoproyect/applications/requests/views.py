from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from applications.requests.model.filter_logic import SearchFilter
from applications.requests.models import Requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@csrf_exempt
def change_requests(request, id):
    if request.method == "POST":
        # Get the request by its ID
        solicitud = get_object_or_404(Requests, pk=id)

        # Get the new status from the POST data
        nuevo_estado = request.POST.get("newStatus")

        # Update the status of the request
        solicitud.status = nuevo_estado
        solicitud.save()

        # Return a successful response
        return JsonResponse(
            {
                "message": f"The status of request {id} has been successfully updated."
            }
        )
    else:
        # If the request is not POST, return an error
        return JsonResponse(
            {"error": "This view only accepts POST requests."}, status=400
        )


def search(request, query):
    # print(query)
    requests_filter = SearchFilter()

    return requests_filter.filter_request(query)


@login_required
def show_requests(request):
    print("Logged user: " + request.user.username)
    # Get all requests assigned to the current user
    if request.user.is_staff:
        requests = Requests.objects.all()
    else:
        requests = Requests.objects.filter(assigned_users = request.user.id)
    return render(request, "show-requests.html", {"requests": requests})


@login_required
def detail_request(request, id):
    detail = Requests.objects.get(pk=id)
    return render(request, "request-detail.html", {"request": detail})
