from django.db import models


class SharePoint(models.Model):
    """
    Model representing SharePoint data.

    Attributes:
        status (str): The status of the SharePoint.
        manager (str): The manager associated with the SharePoint.
        team (int): The team number.
        initial_date (date): The initial date of the SharePoint.
        final_date (date): The final date of the SharePoint.
        fullname (str): The full name of the SharePoint owner.
        faculty (str): The faculty associated with the SharePoint.
        document (str): The document identifier.
        phone_number (str): The phone number of the SharePoint owner.
        email (EmailField): The email address of the SharePoint owner.
        CENCO (str): The CENCO information.
        bank (str): The bank information.
        account_type (str): The account type.
        health_provider (str): The health provider.
        pension_fund (str): The pension fund.
        arl (str): The ARL (Administradora de Riesgos Laborales).
        contract_value (DecimalField): The value of the contract.
        is_one_time_payment (bool): Indicates if it's a one-time payment.
    """
    status = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    team = models.IntegerField()
    initial_date = models.DateField()
    final_date = models.DateField()
    fullname = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    document = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    CENCO = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    health_provider = models.CharField(max_length=100)
    pension_fund = models.CharField(max_length=100)
    arl = models.CharField(max_length=100)
    contract_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_one_time_payment = models.BooleanField()
