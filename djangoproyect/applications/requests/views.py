from django.shortcuts import render


# Create your views here.
def change_requests(request):
    return render(request, "change-requests.html")


def show_requests(request):
    return render(request, "show-requests.html")
