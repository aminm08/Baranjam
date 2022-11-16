from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_group_lists, name='group_lists'),
    path('add/', views.add_group_list_and_send_invitation, name='add_group_list'),
    path('accept_inv/<int:group_id>/<int:inv_id>/', views.accept_invite, name='accept_inv'),

]
