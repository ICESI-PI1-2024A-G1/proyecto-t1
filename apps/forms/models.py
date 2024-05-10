from django.db import models
import json
from django.contrib.auth import get_user_model
from django.apps import apps
from apps.teams.models import Team
from django.utils import timezone

User = get_user_model()


class Form(models.Model):
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=timezone.now)
    member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    status = models.CharField(max_length=200, default="PENDIENTE")
    team_id = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, default=None
    )
    is_reviewed = models.BooleanField(default=False)
    review_data = models.TextField(null=True, blank=True)
    id_person = models.CharField(max_length=200, default="")
    fullname = models.CharField(max_length=200, default="")
    pdf_file = models.FileField(upload_to="filled_forms/", null=True, blank=True, default=None)


    class Meta:
        abstract = True


class TravelAdvanceRequest(Form):
    dependence = models.CharField(max_length=200)
    cost_center = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    departure_date = models.DateField()
    return_date = models.DateField()
    travel_reason = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    expenses = models.TextField()
    signature_status = models.CharField(max_length=200)
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    observations = models.TextField(default="Ninguna")
    signatureInput = models.TextField(null=True, blank=True)

    def set_expenses(self, expenses_dict):
        self.expenses = json.dumps(expenses_dict)

    def get_expenses(self):
        return json.loads(self.expenses)


class TravelExpenseLegalization(Form):
    dependence = models.CharField(max_length=200)
    cost_center = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    departure_date = models.DateField()
    return_date = models.DateField()
    travel_reason = models.TextField()
    total1 = models.DecimalField(max_digits=10, decimal_places=2)
    total2 = models.DecimalField(max_digits=10, decimal_places=2)
    total3 = models.DecimalField(max_digits=10, decimal_places=2)
    advance_total1 = models.DecimalField(max_digits=10, decimal_places=2)
    advance_total2 = models.DecimalField(max_digits=10, decimal_places=2)
    advance_total3 = models.DecimalField(max_digits=10, decimal_places=2)
    employee_balance1 = models.DecimalField(max_digits=10, decimal_places=2)
    employee_balance2 = models.DecimalField(max_digits=10, decimal_places=2)
    employee_balance3 = models.DecimalField(max_digits=10, decimal_places=2)
    icesi_balance1 = models.DecimalField(max_digits=10, decimal_places=2)
    icesi_balance2 = models.DecimalField(max_digits=10, decimal_places=2)
    icesi_balance3 = models.DecimalField(max_digits=10, decimal_places=2)
    signature_status = models.BooleanField()
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    observations = models.TextField(default="Ninguna")
    signatureInput = models.TextField(null=True, blank=True)


class TravelExpenseLegalization_Table(models.Model):
    travel_info = models.ForeignKey(
        TravelExpenseLegalization,
        on_delete=models.CASCADE,
    )
    category = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    nit = models.CharField(max_length=200)
    concept = models.CharField(max_length=200)
    pesos = models.DecimalField(max_digits=10, decimal_places=2)
    dollars = models.DecimalField(max_digits=10, decimal_places=2)
    euros = models.DecimalField(max_digits=10, decimal_places=2)

    def serialize(self):
        return json.dumps(
            {
                "category": self.category,
                "provider": self.provider,
                "nit": self.nit,
                "concept": self.concept,
                "pesos": str(self.pesos),
                "dollars": str(self.dollars),
                "euros": str(self.euros),
            }
        )


class AdvanceLegalization(Form):
    dependence = models.CharField(max_length=200)
    cost_center = models.CharField(max_length=200)
    purchase_reason = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    advance_total = models.DecimalField(max_digits=10, decimal_places=2)
    employee_balance_value = models.DecimalField(max_digits=10, decimal_places=2)
    icesi_balance_value = models.DecimalField(max_digits=10, decimal_places=2)
    signature_status = models.BooleanField()
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    observations = models.TextField(default="Ninguna")
    signatureInput = models.TextField(null=True, blank=True)


class AdvanceLegalization_Table(models.Model):
    general_data = models.ForeignKey(
        AdvanceLegalization,
        on_delete=models.CASCADE,
    )
    category = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    pesos = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.TextField()


class BillingAccount(Form):
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    concept_reason = models.CharField(max_length=200)
    retention = models.CharField(max_length=200)
    tax_payer = models.CharField(max_length=200)
    resident = models.CharField(max_length=200)
    request_city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    signature_status = models.CharField(max_length=200)
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    cex_number = models.CharField(max_length=200)
    signatureInput = models.TextField(null=True, blank=True)


class Requisition(Form):
    work = models.CharField(max_length=200)
    dependence = models.CharField(max_length=200)
    cenco = models.CharField(max_length=200)
    id_value = models.CharField(max_length=200)
    description = models.TextField()
    signature_status = models.BooleanField()
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    observations = models.TextField(default="Ninguna")
    signatureInput = models.TextField(null=True, blank=True)


class Country(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class AccountType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Dependency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class CostCenter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
