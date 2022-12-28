from django.contrib import admin

from .models import Todo, Job


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['name', 'datetime_created', 'user', 'is_group_list']
    Todo.is_group_list.boolean = True


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['text', 'todo', 'user', 'is_done', 'datetime_created', 'user_done_date', 'duration']

    search_fields = ('text', 'user__username','duration', 'user_done_date')
