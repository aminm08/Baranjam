from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_repetitiveness_display', 'start_date',)
    list_filter = ('repetitiveness',)
    search_fields = ('title',)
