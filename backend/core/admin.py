from django.contrib import admin
from .models import PayEmployee, Payslip, Deduction

@admin.register(PayEmployee)
class PayEmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "employee_id", "department", "designation", "basic_salary", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "employee_id", "department"]

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ["employee_name", "month", "year", "gross", "deductions", "created_at"]
    list_filter = ["status"]
    search_fields = ["employee_name", "month"]

@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ["name", "deduction_type", "amount", "percentage", "active", "created_at"]
    list_filter = ["deduction_type"]
    search_fields = ["name"]
