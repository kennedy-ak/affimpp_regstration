from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [


path("",views.landing),
path('admin-login/', views.admin_login, name='admin_login'),
path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),
path('student-dashboard',views.student_dashboard,name='student_dashboard'),
path('student-signup/', views.student_register, name='signup'),

path('register/', views.register, name='register_course'),
  path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
