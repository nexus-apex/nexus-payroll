from django.db import models

class PayEmployee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255, blank=True, default="")
    department = models.CharField(max_length=255, blank=True, default="")
    designation = models.CharField(max_length=255, blank=True, default="")
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    bank_account = models.CharField(max_length=255, blank=True, default="")
    pan_number = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Payslip(models.Model):
    employee_name = models.CharField(max_length=255)
    month = models.CharField(max_length=255, blank=True, default="")
    year = models.IntegerField(default=0)
    gross = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("processed", "Processed"), ("paid", "Paid")], default="draft")
    generated_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.employee_name

class Deduction(models.Model):
    name = models.CharField(max_length=255)
    deduction_type = models.CharField(max_length=50, choices=[("tax", "Tax"), ("pf", "PF"), ("esi", "ESI"), ("insurance", "Insurance"), ("loan", "Loan"), ("other", "Other")], default="tax")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
