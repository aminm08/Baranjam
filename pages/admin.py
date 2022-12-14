from django.contrib import admin
from .models import Contact, Invitation


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'user', 'ip_addr']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['user_sender', 'user_receiver', 'datetime_created']
