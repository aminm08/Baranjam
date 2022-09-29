from django import forms
from django.utils.translation import gettext as _
from jalali_date.fields import SplitJalaliDateTimeField
from jalali_date.admin import AdminSplitJalaliDateTime

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['text', 'user_datetime']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['user_datetime'] = SplitJalaliDateTimeField(label=_('Due date time'), widget=AdminSplitJalaliDateTime)
