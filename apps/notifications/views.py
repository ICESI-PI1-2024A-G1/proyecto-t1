from django.shortcuts import render
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
    if request.user.is_superuser:
        status_notifications = StatusNotification.objects.all().order_by("-id")
        assign_notifications = AssignNotification.objects.all().order_by("-id")
        fill_notifications = FillFormNotification.objects.all().order_by("-id")
        date_notifications = DateChangeNotification.objects.all().order_by("-id")
    else:
        status_notifications = StatusNotification.objects.filter(user_target=request.user).order_by("-id")
        assign_notifications = AssignNotification.objects.filter(user_target=request.user).order_by("-id")
        fill_notifications = FillFormNotification.objects.filter(user_target=request.user).order_by("-id")
        date_notifications = DateChangeNotification.objects.filter(user_target=request.user).order_by("-id")
    for notification in status_notifications:
        notification.prev_color = statusMap[notification.prev_state]
        notification.new_color = statusMap[notification.new_state]

    context = {
        "status_notifications": status_notifications,
        "assign_notifications": assign_notifications,
        "fill_notifications": fill_notifications,
        "date_notifications": date_notifications,
    }
    return render(request, "show_notifications.html", context)