from django.contrib import admin
from .models import GroupList


@admin.register(GroupList)
class GroupListAdmin(admin.ModelAdmin):
    list_display = ['todo']
    search_fields = ['todo', 'users']
