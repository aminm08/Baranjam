from django import forms
from django.utils.translation import gettext as _
from jalali_date.fields import SplitJalaliDateTimeField, JalaliDateTimeField
from jalali_date.admin import AdminSplitJalaliDateTime

from .models import Job, Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('name',)

        error_messages = {
            'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['text', 'user_datetime']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['user_datetime'] = SplitJalaliDateTimeField(label=_('Due date time'),
                                                                widget=AdminSplitJalaliDateTime)
        self.fields['user_datetime'].required = False
        self.fields['text'].required = True
