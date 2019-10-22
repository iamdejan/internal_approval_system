from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomEmployeeCreationForm, CustomEmployeeChangeForm
from .models import *

class CustomEmployeeAdmin(UserAdmin):
    model = Employee
    add_form = CustomEmployeeCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("first_name", "last_name",)
        }),
        ("Additional Data", {
            "fields": ("public_key", "level",)
        }),
    )
    form = CustomEmployeeChangeForm
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Data", {
            "fields": ("public_key", "level",)
        }),
    )
    list_display = ["id", "username", "first_name", "last_name", "level",]

class CustomProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ["title", "checklist_mask", "tail_hash"]
    pass

class CustomContractAdmin(admin.ModelAdmin):
    model = SmartContract
    list_display = ["contract_code", "threshold",]

class CustomApprovalAdmin(admin.ModelAdmin):
    model = Approval
    list_display = ["employee", "hash"]

# Register your models here.
admin.site.register(EmployeeLevel)
admin.site.register(Employee, CustomEmployeeAdmin)
admin.site.register(Approval, CustomApprovalAdmin)
admin.site.register(Project, CustomProjectAdmin)
admin.site.register(SmartContract, CustomContractAdmin)