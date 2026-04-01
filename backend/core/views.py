import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import PayEmployee, Payslip, Deduction


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['payemployee_count'] = PayEmployee.objects.count()
    ctx['payemployee_active'] = PayEmployee.objects.filter(status='active').count()
    ctx['payemployee_inactive'] = PayEmployee.objects.filter(status='inactive').count()
    ctx['payemployee_total_basic_salary'] = PayEmployee.objects.aggregate(t=Sum('basic_salary'))['t'] or 0
    ctx['payslip_count'] = Payslip.objects.count()
    ctx['payslip_draft'] = Payslip.objects.filter(status='draft').count()
    ctx['payslip_processed'] = Payslip.objects.filter(status='processed').count()
    ctx['payslip_paid'] = Payslip.objects.filter(status='paid').count()
    ctx['payslip_total_gross'] = Payslip.objects.aggregate(t=Sum('gross'))['t'] or 0
    ctx['deduction_count'] = Deduction.objects.count()
    ctx['deduction_tax'] = Deduction.objects.filter(deduction_type='tax').count()
    ctx['deduction_pf'] = Deduction.objects.filter(deduction_type='pf').count()
    ctx['deduction_esi'] = Deduction.objects.filter(deduction_type='esi').count()
    ctx['deduction_total_amount'] = Deduction.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['recent'] = PayEmployee.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def payemployee_list(request):
    qs = PayEmployee.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'payemployee_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def payemployee_create(request):
    if request.method == 'POST':
        obj = PayEmployee()
        obj.name = request.POST.get('name', '')
        obj.employee_id = request.POST.get('employee_id', '')
        obj.department = request.POST.get('department', '')
        obj.designation = request.POST.get('designation', '')
        obj.basic_salary = request.POST.get('basic_salary') or 0
        obj.status = request.POST.get('status', '')
        obj.bank_account = request.POST.get('bank_account', '')
        obj.pan_number = request.POST.get('pan_number', '')
        obj.save()
        return redirect('/payemployees/')
    return render(request, 'payemployee_form.html', {'editing': False})


@login_required
def payemployee_edit(request, pk):
    obj = get_object_or_404(PayEmployee, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.employee_id = request.POST.get('employee_id', '')
        obj.department = request.POST.get('department', '')
        obj.designation = request.POST.get('designation', '')
        obj.basic_salary = request.POST.get('basic_salary') or 0
        obj.status = request.POST.get('status', '')
        obj.bank_account = request.POST.get('bank_account', '')
        obj.pan_number = request.POST.get('pan_number', '')
        obj.save()
        return redirect('/payemployees/')
    return render(request, 'payemployee_form.html', {'record': obj, 'editing': True})


@login_required
def payemployee_delete(request, pk):
    obj = get_object_or_404(PayEmployee, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/payemployees/')


@login_required
def payslip_list(request):
    qs = Payslip.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(employee_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'payslip_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def payslip_create(request):
    if request.method == 'POST':
        obj = Payslip()
        obj.employee_name = request.POST.get('employee_name', '')
        obj.month = request.POST.get('month', '')
        obj.year = request.POST.get('year') or 0
        obj.gross = request.POST.get('gross') or 0
        obj.deductions = request.POST.get('deductions') or 0
        obj.net_salary = request.POST.get('net_salary') or 0
        obj.status = request.POST.get('status', '')
        obj.generated_date = request.POST.get('generated_date') or None
        obj.save()
        return redirect('/payslips/')
    return render(request, 'payslip_form.html', {'editing': False})


@login_required
def payslip_edit(request, pk):
    obj = get_object_or_404(Payslip, pk=pk)
    if request.method == 'POST':
        obj.employee_name = request.POST.get('employee_name', '')
        obj.month = request.POST.get('month', '')
        obj.year = request.POST.get('year') or 0
        obj.gross = request.POST.get('gross') or 0
        obj.deductions = request.POST.get('deductions') or 0
        obj.net_salary = request.POST.get('net_salary') or 0
        obj.status = request.POST.get('status', '')
        obj.generated_date = request.POST.get('generated_date') or None
        obj.save()
        return redirect('/payslips/')
    return render(request, 'payslip_form.html', {'record': obj, 'editing': True})


@login_required
def payslip_delete(request, pk):
    obj = get_object_or_404(Payslip, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/payslips/')


@login_required
def deduction_list(request):
    qs = Deduction.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(deduction_type=status_filter)
    return render(request, 'deduction_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def deduction_create(request):
    if request.method == 'POST':
        obj = Deduction()
        obj.name = request.POST.get('name', '')
        obj.deduction_type = request.POST.get('deduction_type', '')
        obj.amount = request.POST.get('amount') or 0
        obj.percentage = request.POST.get('percentage') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/deductions/')
    return render(request, 'deduction_form.html', {'editing': False})


@login_required
def deduction_edit(request, pk):
    obj = get_object_or_404(Deduction, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.deduction_type = request.POST.get('deduction_type', '')
        obj.amount = request.POST.get('amount') or 0
        obj.percentage = request.POST.get('percentage') or 0
        obj.active = request.POST.get('active') == 'on'
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/deductions/')
    return render(request, 'deduction_form.html', {'record': obj, 'editing': True})


@login_required
def deduction_delete(request, pk):
    obj = get_object_or_404(Deduction, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/deductions/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['payemployee_count'] = PayEmployee.objects.count()
    data['payslip_count'] = Payslip.objects.count()
    data['deduction_count'] = Deduction.objects.count()
    return JsonResponse(data)
