from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_measure_display', 'jobs', 'hours',)
    list_filter = ('measure',)
    search_fields = ('user__username',)
