from django.shortcuts import render
from apps.internalRequests.views import get_request_by_id
from apps.notifications.models import StatusNotification, DateChangeNotification, AssignNotification, FillFormNotification
from django.contrib.auth.decorators import login_required

statusMap = {
    "PENDIENTE": "secondary",
    "EN REVISIÓN": "info",
    "POR APROBAR": "primary",
    "DEVUELTO": "warning",
    "RECHAZADO": "danger",
    "RESUELTO": "success",
}

# Create your views here.
@login_required
def show_notifications(request):
    """
    Render the notifications page.
    
    This view function displays notifications based on the user's role:
    - If the user is a superuser, it displays all notifications.
    - If the user is not a superuser, it displays notifications relevant to that user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered notifications page.
    """

    if request.user.is_superuser:
        status_notifications = StatusNotification.objects.all().order_by("-id")
        assign_notifications = AssignNotification.objects.all().order_by("-id")
        fill_notifications = FillFormNotification.objects.all().order_by("-id")
        date_notifications = DateChangeNotification.objects.all().order_by("-id")
    elif request.user.is_leader:
        status_notifications = StatusNotification.objects.filter(user_target=request.user).order_by("-id")
        assign_notifications = AssignNotification.objects.filter(user_target=request.user).order_by("-id")
        fill_notifications = FillFormNotification.objects.filter(user_target=request.user).order_by("-id")
        date_notifications = DateChangeNotification.objects.filter(user_target=request.user).order_by("-id")
    elif request.user.is_member:
        status_notifications = StatusNotification.objects.filter(modified_by=request.user).order_by("-id")
        assign_notifications = AssignNotification.objects.filter(modified_by=request.user).order_by("-id")
        fill_notifications = FillFormNotification.objects.filter(modified_by=request.user).order_by("-id")
        date_notifications = DateChangeNotification.objects.filter(modified_by=request.user).order_by("-id")
    else:
        status_notifications = [ form for form in StatusNotification.objects.all().order_by("-id") if get_request_by_id(form.request_id).id_person == request.user.id]
        assign_notifications = [ form for form in AssignNotification.objects.all().order_by("-id") if get_request_by_id(form.request_id).id_person == request.user.id]
        fill_notifications = [ form for form in FillFormNotification.objects.all().order_by("-id") if get_request_by_id(form.request_id).id_person == request.user.id]
        date_notifications = [ form for form in DateChangeNotification.objects.all().order_by("-id") if get_request_by_id(form.request_id).id_person == request.user.id]
    for notification in status_notifications:
        notification.prev_color = statusMap[notification.prev_state] if notification.prev_state in statusMap else "secondary"
        notification.new_color = statusMap[notification.new_state] if notification.new_state in statusMap else "secondary"
    context = {
        "status_notifications": status_notifications,
        "assign_notifications": assign_notifications,
        "fill_notifications": fill_notifications,
        "date_notifications": date_notifications,
    }
    return render(request, "show_notifications.html", context)