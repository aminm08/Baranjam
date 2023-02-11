from django import forms
from .models import GroupList
from todo.models import Todo
from django.contrib.auth import get_user_model


class GroupListForm(forms.ModelForm):
    todo = forms.ModelMultipleChoiceField(queryset=Todo.objects.all(), widget=forms.CheckboxSelectMultiple,
                                          required=False)
    members = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all(),
                                             widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, user, *args, **kwargs):
        exclude_members = kwargs.pop('exclude_members', False)

        super(GroupListForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['todo'].queryset = user.todos.all()
        self.fields['members'].queryset = get_user_model().objects.exclude(username=user.username)

        if exclude_members:
            del self.fields['members']

    class Meta:
        model = GroupList
        fields = ('title', 'todo', 'members', 'description', 'enable_chat', 'enable_job_divider', 'picture')

    def save(self, create=True):

        if create:
            self.instance.save()

            data = self.cleaned_data
            for todo in data['todo']:
                self.instance.todo.add(todo)
            self.instance.admins.add(self.user)
        else:
            return super(GroupListForm, self).save()

        return self.instance
