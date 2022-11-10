from django import forms
from django.utils.translation import gettext as _
from jalali_date.fields import JalaliDateField
from jalali_date.admin import AdminJalaliDateWidget
from crispy_forms.helper import FormHelper
from .models import Job, Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('name',)

        error_messages = {
            'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
        }


class JobTimeInputWidget(forms.TimeInput):
    input_type = 'time'


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['text', 'user_date', 'user_time']
        widgets = {
            'user_time': JobTimeInputWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['user_date'] = JalaliDateField(label=_('Due date time'), widget=AdminJalaliDateWidget,
                                                   required=False)
        self.fields['text'].required = True


