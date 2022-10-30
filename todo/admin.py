from django.contrib import admin

from .models import Todo, Job


class JobInline(admin.TabularInline):
    model = Job


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['name', 'datetime_created', 'user']
    inlines = [JobInline, ]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['text', 'todo', 'user', 'is_done', 'datetime_created']

    search_fields = ('text', 'user__username',)
