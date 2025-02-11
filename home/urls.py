# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_test, name='start_test'),
    path('clear/', views.clear_cache, name='clear_cache'),
    path('result/', views.result, name='result'),
    path('delete/<str:id>/', views.delete_user, name='delete_user'),
    # 6ae92f32-d3bc-4f55-bf39-44c7f9001fbd test ref ID
]