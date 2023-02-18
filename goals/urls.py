from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.GoalCreateView.as_view(), name='goal_create'),
    path('delete/<int:pk>/', views.GoalDeleteView.as_view(), name='goal_delete'),
]
