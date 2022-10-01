from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'profile_picture', 'mobile_number', 'address', 'task_completed')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birth_date', 'profile_picture', 'mobile_number', 'address', 'task_completed')}),
    )

    list_display = ['username', 'email', ]
