from django.contrib import admin
from .models import (TravelAdvanceRequest, TravelExpenseLegalization, 
                     TravelExpenseLegalization_Table, AdvanceLegalization, 
                     AdvanceLegalization_Table, BillingAccount, Requisition, 
                     Country, City, Bank, AccountType, Dependency, CostCenter)

class TravelAdvanceRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TravelAdvanceRequest._meta.fields]

class TravelExpenseLegalizationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TravelExpenseLegalization._meta.fields]

class TravelExpenseLegalization_TableAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TravelExpenseLegalization_Table._meta.fields]

class AdvanceLegalizationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdvanceLegalization._meta.fields]

class AdvanceLegalization_TableAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdvanceLegalization_Table._meta.fields]

class BillingAccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BillingAccount._meta.fields]

class RequisitionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Requisition._meta.fields]

class CountryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Country._meta.fields]

class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]

class BankAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bank._meta.fields]

class AccountTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AccountType._meta.fields]

class DependencyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Dependency._meta.fields]

class CostCenterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CostCenter._meta.fields]

admin.site.register(TravelAdvanceRequest, TravelAdvanceRequestAdmin)
admin.site.register(TravelExpenseLegalization, TravelExpenseLegalizationAdmin)
admin.site.register(TravelExpenseLegalization_Table, TravelExpenseLegalization_TableAdmin)
admin.site.register(AdvanceLegalization, AdvanceLegalizationAdmin)
admin.site.register(AdvanceLegalization_Table, AdvanceLegalization_TableAdmin)
admin.site.register(BillingAccount, BillingAccountAdmin)
admin.site.register(Requisition, RequisitionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Dependency, DependencyAdmin)
admin.site.register(CostCenter, CostCenterAdmin)