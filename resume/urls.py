# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.resume_dashboard, name='resume_dashboard'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('add-job/', views.add_job, name='add_job'),
    path('delete_resume/<int:id>/', views.delete_resume, name='delete_resume'),
]