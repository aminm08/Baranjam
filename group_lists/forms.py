from django import forms
from .models import GroupList
from todo.models import Todo


class GroupListForm(forms.ModelForm):
    todo = forms.ModelMultipleChoiceField(queryset=Todo.objects.all(), widget=forms.CheckboxSelectMultiple,required=False)

    def __init__(self, user, *args, **kwargs):
        super(GroupListForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['todo'].queryset = user.todos.all()

    class Meta:
        model = GroupList
        fields = ('title', 'todo', 'description', 'enable_chat', 'enable_job_divider', 'picture')

    def save_todo_m2m_and_add_admin(self):
        # saving m2ms manually
        data = self.cleaned_data
        for todo in data['todo']:
            self.instance.todo.add(todo)
        self.instance.admins.add(self.user)

        return self.instance
