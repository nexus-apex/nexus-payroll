from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import PayEmployee, Payslip, Deduction
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusPayroll with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuspayroll.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if PayEmployee.objects.count() == 0:
            for i in range(10):
                PayEmployee.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    employee_id=f"Sample {i+1}",
                    department=f"Sample {i+1}",
                    designation=f"Sample {i+1}",
                    basic_salary=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["active", "inactive"]),
                    bank_account=f"Sample {i+1}",
                    pan_number=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 PayEmployee records created'))

        if Payslip.objects.count() == 0:
            for i in range(10):
                Payslip.objects.create(
                    employee_name=f"Sample Payslip {i+1}",
                    month=f"Sample {i+1}",
                    year=random.randint(1, 100),
                    gross=round(random.uniform(1000, 50000), 2),
                    deductions=round(random.uniform(1000, 50000), 2),
                    net_salary=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["draft", "processed", "paid"]),
                    generated_date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 Payslip records created'))

        if Deduction.objects.count() == 0:
            for i in range(10):
                Deduction.objects.create(
                    name=f"Sample Deduction {i+1}",
                    deduction_type=random.choice(["tax", "pf", "esi", "insurance", "loan", "other"]),
                    amount=round(random.uniform(1000, 50000), 2),
                    percentage=round(random.uniform(1000, 50000), 2),
                    active=random.choice([True, False]),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Deduction records created'))
