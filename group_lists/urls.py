from django.urls import path

from . import views

urlpatterns = [
    path('', views.add_user_with_invite_to_group_list_view, name='add_group_list'),
    path('search_view/', views.search_view, name='s_view'),
    path('accept_inv/<int:group_id>/', views.accept_invite, name='accept_inv'),
]
