from django.urls import path
from . import views

urlpatterns = [
    path('', views.HabitListView.as_view(), name='habit-list'),
    path('create/', views.habit_create_view, name='habit-create'),
    path('update/<int:pk>/', views.habit_update_view, name='habit-update'),
    path('delete/<int:pk>/', views.HabitDeleteView.as_view(), name='habit-delete'),
]
