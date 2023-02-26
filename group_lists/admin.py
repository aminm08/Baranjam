from django.contrib import admin
from .models import GroupList, Invitation


@admin.register(GroupList)
class GroupListAdmin(admin.ModelAdmin):
    list_display = ['picture_preview', 'title', 'get_all_members_length', 'enable_chat', 'uuid']
    search_fields = ['todo__name', 'members__username', 'admins__username', 'title']
    list_filter = ('enable_chat',)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_sender', 'user_receiver', 'group_list', 'datetime_created']
