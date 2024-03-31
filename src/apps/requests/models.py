"""
Request's models

This module defines Django models for handling requests and their related data.
"""
from django.db import models
from django.conf import settings


class Involved(models.Model):
    """
    Class: Involved

    Model representing individuals involved in requests.

    Attributes:
        email (str): Email of the involved individual.
        name (str): Name of the involved individual.
    """
    email = models.CharField(max_length=320)
    name = models.CharField(max_length=50)

class Requests(models.Model):
    """
    Class: Requests

    Model representing requests.

    Attributes:
        document (str): Document associated with the request.
        applicant (str): Applicant of the request.
        manager (str): Manager handling the request.
        description (str): Description of the request.
        title (str): Title of the request.
        initial_date (date): Initial date of the request.
        final_date (date): Final date of the request.
        past_days (int): Number of past days since the request was made.
        status (str): Current status of the request.
        assigned_users (ManyToManyField): Users assigned to the request.
    """

    document = models.CharField(max_length=255)
    applicant = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=100, null=True)
    initial_date = models.DateField()
    final_date = models.DateField()
    past_days = models.IntegerField()
    status = models.CharField(max_length=20)
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="requests"
    )


class Traceability(models.Model):
    """
    Class: Traceability

    Model representing traceability of requests.

    Attributes:
        modified_by (ForeignKey): User who modified the request.
        request (str): Request associated with the traceability.
        date (date): Date of the traceability.
        reason (str): Reason for the modification.
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
    reason = models.CharField(max_length=70, null=True)
    prev_state = models.CharField(max_length=50, null=True)
    new_state = models.CharField(max_length=50, default=None)
