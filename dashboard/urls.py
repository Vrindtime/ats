# urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # dashboard urls
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('login/', auth_views.LoginView.as_view(next_page='admin_dashboard'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<str:id>/', views.approve_view, name='approve_view'),
    path('reject/<str:id>/', views.reject_view, name='reject_view'),
]
