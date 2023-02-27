from django.urls import path

from . import views

urlpatterns = [
    path('group_online_users/<int:group_id>/', views.get_group_online_users, name='group_online_users'),
    path('delete_all/<int:group_id>/', views.delete_group_chat, name='delete_chats'),
]
