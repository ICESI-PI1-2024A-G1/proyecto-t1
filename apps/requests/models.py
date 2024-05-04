from django.db import models


class SharePoint(models.Model):
    status = models.CharField(max_length=50)
    manager = models.CharField(max_length=100)
    team = models.IntegerField()
    initial_date = models.DateField()
    final_date = models.DateField()
    fullname = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    document = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    CENCO = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    health_provider = models.CharField(max_length=100)
    pension_fund = models.CharField(max_length=100)
    arl = models.CharField(max_length=100)
    contract_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_one_time_payment = models.BooleanField()
