from django.http import HttpResponse

# Create your views here.
def requests(request):
    return HttpResponse("Requests")