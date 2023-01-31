from django import forms

from .models import GroupList
from todo.models import Todo
from django.contrib.auth import get_user_model


class GroupListForm(forms.ModelForm):
    todo = forms.ModelMultipleChoiceField(queryset=Todo.objects.all(), widget=forms.CheckboxSelectMultiple)
    members = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, user, *args, **kwargs):
        super(GroupListForm, self).__init__(*args, **kwargs)
        self.fields['todo'].queryset = user.todos.all()
        self.fields['members'].queryset = get_user_model().objects.exclude(username=user.username)

    class Meta:
        model = GroupList
        fields = ('title', 'todo', 'members', 'description', 'enable_chat', 'enable_job_divider', 'picture')
