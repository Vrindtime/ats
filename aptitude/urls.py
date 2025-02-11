from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='aptitude_dashboard'),
    path('addQuestions/', views.add_aptitude_questions, name='add_aptitude_questions'),
    path('addCategory/', views.add_aptitude_category, name='add_aptitude_category'),
    path('test/', views.aptitude_test, name='aptitude_test'),
    path('submit-test/', views.submit_test, name='submit_test'),
    path('edit_aptitude/<int:id>/', views.edit_aptitude, name='edit_aptitude'),
    path('delete_aptitude/<int:id>/', views.delete_aptitude, name='delete_aptitude'),
]
