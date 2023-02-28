from django.urls import path, re_path

from . import views

urlpatterns = [
    # CRUD
    path('', views.user_group_lists, name='group_lists'),
    path('<int:pk>/', views.user_group_details, name='group_detail'),
    path('create/', views.create_group, name='group_create'),
    path('delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('update/<int:group_id>/', views.group_update_view, name='group_update'),
    # endpoint
    path('manage_admins/<int:group_id>/', views.manage_group_members_grade, name='manage_members_grade'),
    path('leave_group/<int:group_id>/', views.leave_group_view, name='leave_group'),
    path('remove_member/<int:group_id>/', views.remove_user_from_group, name='remove_group_member'),
    # invitation
    path('invite/users/<int:group_id>/', views.invite_new_members, name='invite_members'),
    path('invite/accept/<int:group_id>/<int:inv_id>/', views.accept_invite, name='accept_inv'),
    re_path('invite/accept_foreign/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.foreign_invitation_show_info,
            name='foreign_inv_show_info'),
    path('invite/accept_foreign/<int:group_id>/', views.accept_foreign_invite_view, name='accept_inv_foreign'),

    path('search_view/<int:group_id>/', views.group_invite_user_search_view, name='search_users_view'),

]
