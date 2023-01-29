from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_group_lists, name='group_lists'),
    path('create/', views.GroupCreateView.as_view(), name='group_create'),
    path('add/', views.add_group_list_and_send_invitation, name='add_group_list'),
    path('leave_group/<int:group_id>/', views.leave_group_view, name='leave_group'),
    path('delete_user/<int:group_id>/', views.remove_user_from_list, name='delete_group_user'),
    path('accept_inv/<int:group_id>/<int:inv_id>/', views.accept_invite, name='accept_inv'),
    path('search_view/', views.search_view, name='search_users_view'),

]
