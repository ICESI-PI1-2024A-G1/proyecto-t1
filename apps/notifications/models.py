from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    """
    Class: Notification

    Model representing notification of requests.

    Attributes:
        user_target (ForeignKey): User who will receive the notification.
        modified_by (ForeignKey): User who modified the request.
        request (str): Request associated with the notification.
        date (date): Date of the notification.
    """
    user_target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="target",
        default=None,
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender",
        default=None,
    )
    request_id = models.CharField(max_length=10)
    date = models.DateField()

class AssignNotification(Notification):
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name="team", default=None)

class StatusNotification(Notification):
    prev_state = models.CharField(max_length=50, null=True, default=None)
    new_state = models.CharField(max_length=50, null=True, default=None)
    reason = models.CharField(max_length=100, null=True, default=None)

class FillFormNotification(Notification):
    pdf_link = models.CharField(max_length=100, null=True, default=None)
    form_type = models.CharField(max_length=50, null=True, default=None)

class DateChangeNotification(Notification):
    prev_date = models.DateField()
    new_date = models.DateField()