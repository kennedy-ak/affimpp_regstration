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
#     path('initiate-payment/<int:registration_id>/', views.initiate_payment, name='initiate_payment'),
#     path('payment/callback/', views.payment_callback, name='payment_callback'),
 ]
