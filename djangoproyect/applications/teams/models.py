from django.db import models


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.IntegerField()

    def __str__(self):
        return self.name
