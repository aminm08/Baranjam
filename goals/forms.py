from django import forms
from django.utils.translation import gettext as _
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('measure', 'jobs', 'hours',)
