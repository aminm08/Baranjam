from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    re_path(r'todo_list/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.todo_list_main_page, name='todo_list'),
    re_path(r'todo_list/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/(?P<job_id>[0-9]+)/$', views.job_update_view,
            name='job_update'),
    path('', views.all_user_todos, name='user_todos'),
    path('update_name/<int:pk>/', views.todo_update_list_name, name='update_todo_name'),
    path('add/', views.AddTodo.as_view(), name='add_todo'),
    path('settings/<int:pk>/', views.todo_list_detail_and_settings, name='todo_settings'),

    path('job/create/<int:todo_id>/', views.CreateJobView.as_view(), name='job_create'),
    path('job/delete/<int:pk>/', views.JobDeleteView.as_view(), name='job_delete'),
    re_path('delete/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.TodoDeleteView.as_view(), name='todo_delete'),
    path('apply/<int:pk>/', views.todo_apply_options_post_view, name='apply_todo_actions'),

]
