from rest_framework.routers import SimpleRouter
from django.urls import path

from . import views

urlpatterns = [
    path('todo/', views.TodoList.as_view(), name='api_todo_list'),
    path('todo/<int:pk>/', views.TodoDetail.as_view(), name='api_todo_detail'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='api_user_detail'),
    path('', views.Hello.as_view(), name='hi'),

]
