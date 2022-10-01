from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'todo_list/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.todo_list_main_page, name='todo_list'),
    path('', views.all_user_todos, name='user_todos'),
    path('add/', views.AddTodo.as_view(), name='add_todo'),
    path('job/create/<int:todo_id>/', views.CreateJobView.as_view(), name='job_create'),
    path('job/delete/<int:pk>/', views.JobDeleteView.as_view(), name='job_delete'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='todo_delete'),

    #pdf render
    path('pdf/<int:todo_id>/', views.render_pdf, name='pdf')

]
