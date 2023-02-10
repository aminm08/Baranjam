from django.contrib import admin

from .models import OnlineUsers, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'text', 'datetime_created',)
    search_fields = ('group__title', 'user__username', 'text')


@admin.register(OnlineUsers)
class OnlineUsersAdmin(admin.ModelAdmin):
    list_display = ('group', 'get_online_users_length',)
    search_fields = ('group__title', 'online_users__username',)
