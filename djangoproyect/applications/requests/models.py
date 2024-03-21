from django.db import models
from django.contrib.auth.models import User


class Involved(models.Model):
    email = models.CharField(max_length=320)
    name = models.CharField(max_length=50)


# Create your models here.
class Requests(models.Model):
    document = models.CharField(max_length=255)
    applicant = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=100, null=True)
    initial_date = models.DateField()
    final_date = models.DateField()
    past_days = models.IntegerField()
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    assigned_users = models.ManyToManyField(User, related_name="requests")


class Traceability(models.Model):
    involved = models.ForeignKey(Involved, on_delete=models.CASCADE)
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    date = models.DateField()
