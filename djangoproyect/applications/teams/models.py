from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="leading_teams"
    )
    members = models.ManyToManyField(User, related_name="teams")

    def __str__(self):
        return self.name
