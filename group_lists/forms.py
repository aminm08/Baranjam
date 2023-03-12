from django import forms
from .models import GroupList
from todo.models import Todo
from django.utils.translation import gettext_lazy as _


class GroupListForm(forms.ModelForm):
    todos = forms.ModelMultipleChoiceField(label=_("Your Todo-lists"), queryset=Todo.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False)
    title = forms.CharField(label=_('Group title'), widget=forms.TextInput(attrs={'placeholder': _('Title')}))

    def __init__(self, user, *args, **kwargs):
        super(GroupListForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['todos'].queryset = user.todos.all()
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 5})

    class Meta:
        model = GroupList
        fields = ('title', 'todos', 'description', 'enable_chat', 'enable_job_divider', 'picture')

    def save_todo_m2m_and_add_admin(self):
        # saving m2ms manually
        data = self.cleaned_data
        for todo in data['todos']:
            self.instance.todos.add(todo)
        self.instance.admins.add(self.user)

        return self.instance
