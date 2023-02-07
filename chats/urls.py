from django.urls import path

from . import views

urlpatterns = [
    path('group_online_users/<int:group_id>/', views.get_group_online_users, name='group_online_users'),
]
