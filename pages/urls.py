from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
    path('about_us/', views.about_us, name='about_us')
]
