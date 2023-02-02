from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_group_lists, name='group_lists'),
    path('<int:pk>/', views.user_group_details, name='group_detail'),
    path('create/', views.create_group, name='group_create'),
    path('delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('update/<int:pk>/', views.group_update_view,  name='group_update'),
    path('add_admin/<int:group_id>/', views.AddGroupAdmin.as_view(), name='add_admin'),
    path('leave_group/<int:group_id>/', views.leave_group_view, name='leave_group'),
    path('delete_user/<int:group_id>/', views.remove_user_from_list, name='delete_group_user'),
    path('accept_inv/<int:group_id>/<int:inv_id>/', views.accept_invite, name='accept_inv'),
    path('search_view/', views.search_view, name='search_users_view'),

]
