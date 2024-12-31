from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [


path("",views.landing,name="landing"),
path('admin-login/', views.admin_login, name='admin_login'),
path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),
path('student-dashboard',views.student_dashboard,name='student_dashboard'),
path('student-signup/', views.student_register, name='signup'),
path('export-registrations/', views.export_registrations_with_files, name='export_registrations_with_files'),

path('register/', views.register, name='register_course'),
path('login/', views.custom_login, name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
path('pay/<int:registration_id>/', views.pay_with_paystack, name='pay_with_paystack'),
path('payment/callback/', views.payment_callback, name='payment_callback'),

  
    # Password reset URLs
   path('password-reset/', auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'), name='password_reset_complete'),
 
 
 
 ]
