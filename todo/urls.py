from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_user_todos, name='user_todos'),
    path('todo_list/<slug:todo_slug>/', views.todo_list_main_page, name='todo_list'),
    path('add/', views.AddTodo.as_view(), name='add_todo'),
    path('job/create/<int:todo_id>/', views.CreateJobView.as_view(), name='job_create'),
    path('job/delete/<int:pk>/', views.JobDeleteView.as_view(), name='job_delete')

]
