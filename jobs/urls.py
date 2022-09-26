from django.urls import path

from . import views
from .forms import JobFilter

urlpatterns = [
    path('', views.todo_main_page, name='todo_list'),
    path('job/create/', views.CreateJobView.as_view(), name='job_create'),
    path('job/delete/<int:pk>/',views.JobDeleteView.as_view(), name='job_delete')
]
