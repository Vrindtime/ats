# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # personality urls
    path('dashboard/', views.personality_dashboard, name='personality_dashboard'),
    path('add-question/', views.add_question, name='add_question'),
    path('add-choice/<int:question_id>/', views.add_choice, name='add_choice'),
    path('test/', views.personality_test, name='personality_test'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-question/<int:id>/',views.edit_question,name='edit_question'),
    path('delete-question/<int:id>/',views.delete_question,name='delete_question'),
    path('delete-choice/<int:id>/',views.delete_choice,name='delete_choice'),
]
