from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_goal/', views.GoalCreateView.as_view(), name='goal_create'),
]
