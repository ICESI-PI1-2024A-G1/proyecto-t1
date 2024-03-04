from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from applications.requests.models import Requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def change_requests(request, id):
    if request.method == 'POST':
        # Obtener la solicitud por su ID
        solicitud = get_object_or_404(Requests, pk=id)
        
        # Obtener el nuevo estado de los datos POST
        nuevo_estado = request.POST.get('newStatus')
        
        # Actualizar el estado de la solicitud
        solicitud.status = nuevo_estado
        solicitud.save()
        
        # Devolver una respuesta exitosa
        return JsonResponse({'message': f'El estado de la solicitud {id} ha sido actualizado correctamente.'})
    else:
        # Si la solicitud no es POST, devolver un error
        return JsonResponse({'error': 'Esta vista solo acepta solicitudes POST.'}, status=400)



def show_requests(request):
    requests = Requests.objects.all()
    return render(request, "show-requests.html", {"requests": requests})
