from django.shortcuts import render
from apps.notifications.models import StatusNotification, DateChangeNotification, AssignNotification, FillFormNotification

# Create your views here.
def show_notifications(request):
    status_notifications = StatusNotification.objects.all()
    assign_notifications = AssignNotification.objects.all()
    fill_notifications = FillFormNotification.objects.all()
    date_notifications = DateChangeNotification.objects.all()
    context = {
        "status_notifications": status_notifications,
        "assign_notifications": assign_notifications,
        "fill_notifications": fill_notifications,
        "date_notifications": date_notifications,
    }
    return render(request, "show_notifications.html", context)