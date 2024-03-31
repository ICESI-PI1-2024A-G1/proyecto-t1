"""
Request's models

This module defines Django models for handling teams and their related data.
"""

from django.db import models
from django.conf import settings


class Team(models.Model):
    """
    Model representing a team.

    Attributes:
        name (CharField): The name of the team (max length: 100 characters).
        description (TextField): A description of the team.
        created_at (DateTimeField): The date and time when the team was created (auto-generated).
        leader (OneToOneField): The leader of the team (linked to AUTH_USER_MODEL).
        members (ManyToManyField): Members of the team (linked to AUTH_USER_MODEL).

    Methods:
        __str__(): Returns a string representation of the team (its name).

    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leading_team"
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")

    def __str__(self):
        return self.name
