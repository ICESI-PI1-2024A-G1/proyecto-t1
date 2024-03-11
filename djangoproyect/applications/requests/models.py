from django.db import models

class Involved(models.Model):
    email = models.CharField(max_length=320)  
    name = models.CharField(max_length=50)  

# Create your models here.
class Requests(models.Model):
    document = models.CharField(max_length=255)
    applicant = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    initial_date = models.DateField()
    final_date = models.DateField()
    past_days = models.IntegerField()
    status = models.CharField(max_length=20)
    beneficiary = models.ForeignKey(Involved, on_delete=models.CASCADE, related_name="beneficiario")
    reviewer = models.ForeignKey(Involved, on_delete=models.CASCADE, related_name="revisor")
    final_approver = models.ForeignKey(Involved, on_delete=models.CASCADE, related_name="aprobador_final")


class Traceability(models.Model):
    involved = models.ForeignKey(Involved, on_delete=models.CASCADE)
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    date = models.DateField()
