from django.contrib import admin

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_sender', 'user_receiver', 'group_list', 'datetime_created']
