from django.db import models
from django.conf import settings

class Traceability(models.Model):
    """
    Class: Traceability

    Model representing traceability of requests.

    Attributes:
        modified_by (ForeignKey): User who modified the request.
        request (str): Request associated with the traceability.
        date (date): Date of the traceability.
        prev_state (str): Previous state of the request.
        new_state (str): New state of the request.
    """
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="modifier",
        default=None,
    )
    request = models.CharField(max_length=10)
    date = models.DateField()
    prev_state = models.CharField(max_length=50, null=True)
    new_state = models.CharField(max_length=50, default=None)