from django.db import models
import json
from django.contrib.auth import get_user_model
from django.apps import apps
from apps.teams.models import Team
from django.utils import timezone

User = get_user_model()


class Form(models.Model):
    """
    Abstract base class for various forms.

    This class defines common fields and behavior shared by multiple form models.
    """
    id = models.AutoField(primary_key=True)
    request_date = models.DateField()
    final_date = models.DateField(null=True, default=timezone.now)
    signatureInput = models.TextField(null=True, blank=True)
    signature_status = models.BooleanField()
    bank = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
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
    """
    Model for travel advance requests.

    This class represents the model for travel advance requests,
    which includes fields specific to this type of form.
    """

    dependence = models.CharField(max_length=200)
    cost_center = models.CharField(max_length=200)
    destination_city = models.CharField(max_length=200)
    departure_date = models.DateField()
    return_date = models.DateField()
    travel_reason = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    expenses = models.TextField()
    observations = models.TextField(default="Ninguna")

    def set_expenses(self, expenses_dict):
        """Set expenses as a JSON string."""
        self.expenses = json.dumps(expenses_dict)

    def get_expenses(self):
        """Get expenses as a Python dictionary."""
        return json.loads(self.expenses)


class TravelExpenseLegalization(Form):
    """
    Model for travel expense legalization.

    This class represents the model for travel expense legalization forms.
    """
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
    observations = models.TextField(default="Ninguna")


class TravelExpenseLegalization_Table(models.Model):
    """
    Model for travel expense legalization table entries.

    This class represents the model for individual entries in the travel expense legalization table.
    """
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
        """Serialize the model instance into a JSON string."""
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
    """
    Model for advance legalization.

    This class represents the model for advance legalization forms.
    """
    dependence = models.CharField(max_length=200)
    cost_center = models.CharField(max_length=200)
    purchase_reason = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    advance_total = models.DecimalField(max_digits=10, decimal_places=2)
    employee_balance_value = models.DecimalField(max_digits=10, decimal_places=2)
    icesi_balance_value = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.TextField(default="Ninguna")


class AdvanceLegalization_Table(models.Model):
    """
    Model for entries in advance legalization tables.

    This class represents individual entries in the advance legalization tables.
    """
    general_data = models.ForeignKey(
        AdvanceLegalization,
        on_delete=models.CASCADE,
    )
    category = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    pesos = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.TextField()


class BillingAccount(Form):
    """
    Model for billing accounts.

    This class represents billing accounts, which are used for billing purposes.
    """
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    concept_reason = models.CharField(max_length=200)
    retention = models.CharField(max_length=200)
    tax_payer = models.CharField(max_length=200)
    resident = models.CharField(max_length=200)
    request_city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    cex_number = models.CharField(max_length=200)


class Requisition(Form):
    """
    Model for requisitions.

    This class represents requisitions, which are formal requests for items or services.
    """
    work = models.CharField(max_length=200)
    dependence = models.CharField(max_length=200)
    cenco = models.CharField(max_length=200)
    id_value = models.CharField(max_length=200)
    description = models.TextField()
    observations = models.TextField(default="Ninguna")


class Country(models.Model):
    """
    Model for countries.

    This class represents countries, with a code and name as attributes.
    """
    code = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)


class City(models.Model):
    """
    Model for cities.

    This class represents cities, with a country foreign key and a name attribute.
    """
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Bank(models.Model):
    """
    Model for banks.

    This class represents banks, with a name attribute.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class AccountType(models.Model):
    """
    Model for account types.

    This class represents account types, with a name attribute.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Dependency(models.Model):
    """
    Model for dependencies.

    This class represents dependencies, with a name attribute.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class CostCenter(models.Model):
    """
    Model for cost centers.

    This class represents cost centers, with a name attribute.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)