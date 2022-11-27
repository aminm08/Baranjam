from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.admin import AdminJalaliDateWidget


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['profile_picture', 'email', 'username', 'first_name', 'last_name']
