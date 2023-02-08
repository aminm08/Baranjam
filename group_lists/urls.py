from django.urls import path, re_path

from . import views

urlpatterns = [
    # CRUD
    path('', views.user_group_lists, name='group_lists'),
    path('<int:pk>/', views.user_group_details, name='group_detail'),
    path('create/', views.create_group, name='group_create'),
    path('delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('update/<int:group_id>/', views.group_update_view, name='group_update'),

    path('manage_admins/<int:group_id>/', views.manage_admins, name='manage_admins'),
    path('leave_group/<int:group_id>/', views.leave_group_view, name='leave_group'),
    path('remove_member/<int:group_id>/', views.remove_user_from_list, name='remove_group_member'),
    # invitation
    path('invite/users/<int:group_id>/', views.invite_new_members, name='invite_members'),
    path('invite/accept/<int:group_id>/<int:inv_id>/', views.accept_invite, name='accept_inv'),
    re_path('invite/accept_foreign/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.foreign_invitation_accept_view,
            name='foreign_inv_accept_page'),

    path('search_view/', views.search_view, name='search_users_view'),

]
