from django.db import models
import json


class TravelAdvanceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=None)
    traveler_name = models.CharField(max_length=200)
    id_person = models.CharField(max_length=200, default="")
    member_name = models.CharField(max_length=200, null=True, default=None)
    status = models.CharField(max_length=200, default="EN REVISIÓN")
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
    observations = models.TextField()
    team_id = models.IntegerField(default=0)
    signatureInput = models.TextField(null=True, blank=True)

    def set_expenses(self, expenses_dict):
        self.expenses = json.dumps(expenses_dict)

    def get_expenses(self):
        return json.loads(self.expenses)


class TravelExpenseLegalization(models.Model):
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=None)
    traveler_name = models.CharField(max_length=200)
    id_person = models.CharField(max_length=200, default="")
    member_name = models.CharField(max_length=200, null=True, default=None)
    status = models.CharField(max_length=200, default="EN REVISIÓN")
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
    observations = models.TextField()
    team_id = models.IntegerField(default=0)
    signatureInput = models.TextField(null=True, blank=True)


class TravelExpenseLegalization_Table(models.Model):
    travel_info = models.ForeignKey(TravelExpenseLegalization, on_delete=models.CASCADE)
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


class AdvanceLegalization(models.Model):
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=None)
    traveler_name = models.CharField(max_length=200)
    id_person = models.CharField(max_length=200, default="")
    member_name = models.CharField(max_length=200, null=True, default=None)
    status = models.CharField(max_length=200, default="EN REVISIÓN")
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
    observations = models.TextField()
    team_id = models.IntegerField(default=0)
    signatureInput = models.TextField(null=True, blank=True)


class AdvanceLegalization_Table(models.Model):
    general_data = models.ForeignKey(AdvanceLegalization, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    pesos = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.TextField()


class BillingAccount(models.Model):
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=None)
    full_name = models.CharField(max_length=200)
    id_person = models.CharField(max_length=200, default="")
    member_name = models.CharField(max_length=200, null=True, default=None)
    status = models.CharField(max_length=200, default="EN REVISIÓN")
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
    team_id = models.IntegerField(default=0)
    signatureInput = models.TextField(null=True, blank=True)


class Requisition(models.Model):
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=None)
    requester_name = models.CharField(max_length=200)
    id_person = models.CharField(max_length=200, default="")
    member_name = models.CharField(max_length=200, null=True, default=None)
    status = models.CharField(max_length=200, default="EN REVISIÓN")
    work = models.CharField(max_length=200)
    dependence = models.CharField(max_length=200)
    cenco = models.CharField(max_length=200)
    id_value = models.CharField(max_length=200)
    description = models.TextField()
    signature_status = models.BooleanField()
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    observations = models.TextField()
    team_id = models.IntegerField(default=0)
    signatureInput = models.TextField(null=True, blank=True)
