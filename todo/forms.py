from django import forms
from django.utils.translation import gettext as _
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.admin import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from crispy_forms.helper import FormHelper
from .models import Job, Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('name',)


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['text', 'user_date', 'duration', 'user_done_date', 'notes']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        self.fields['user_date'] = JalaliDateField(label=_('Due date time'), widget=AdminJalaliDateWidget,
                                                   required=False)
        self.fields['text'].required = True

        self.fields['notes'].required = False
