from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('payemployees/', views.payemployee_list, name='payemployee_list'),
    path('payemployees/create/', views.payemployee_create, name='payemployee_create'),
    path('payemployees/<int:pk>/edit/', views.payemployee_edit, name='payemployee_edit'),
    path('payemployees/<int:pk>/delete/', views.payemployee_delete, name='payemployee_delete'),
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('payslips/create/', views.payslip_create, name='payslip_create'),
    path('payslips/<int:pk>/edit/', views.payslip_edit, name='payslip_edit'),
    path('payslips/<int:pk>/delete/', views.payslip_delete, name='payslip_delete'),
    path('deductions/', views.deduction_list, name='deduction_list'),
    path('deductions/create/', views.deduction_create, name='deduction_create'),
    path('deductions/<int:pk>/edit/', views.deduction_edit, name='deduction_edit'),
    path('deductions/<int:pk>/delete/', views.deduction_delete, name='deduction_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
