from django import forms

from .models import GroupList
from todo.models import Todo
from django.contrib.auth import get_user_model


class GroupListForm(forms.ModelForm):

    class Meta:
        model = GroupList
        fields = ('title', 'todo', 'users',)
