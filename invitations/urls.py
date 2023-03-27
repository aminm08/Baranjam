from django.urls import path, re_path

from . import views

urlpatterns = [

    re_path('invite/accept_foreign/(?P<signed_pk>[0-9]+/[A-Za-z0-9_=-]+)/$', views.foreign_invitation_show_info,
            name='foreign_inv_show_info'),
    path('invite/users/<int:group_id>/', views.invite_new_members, name='invite_members'),
    path('invite/accept/<int:group_id>/<int:inv_id>/', views.accept_invite, name='accept_inv'),
    path('invite/accept_foreign/<int:group_id>/', views.accept_foreign_invite_view, name='accept_inv_foreign'),
    path('invite/delete/<int:inv_id>/', views.delete_invitation_view, name='delete_inv'),

]
