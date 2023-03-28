from django import forms
from django.utils.translation import gettext_lazy as _
from jalali_date.admin import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField
from django.utils import timezone
from .models import Habit


class HabitForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['todo_list'].queryset = user.todos.all().order_by('-datetime_created')
        self.fields['start_date'] = JalaliDateField(label=_('Habit start date'), widget=AdminJalaliDateWidget,
                                                    required=True, initial=timezone.now)
        self.fields['end_date'] = JalaliDateField(label=_('Habit end date'), widget=AdminJalaliDateWidget,
                                                  required=False)
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 5})

    class Meta:
        model = Habit
        fields = ('title', 'description', 'todo_list', 'repetitiveness', 'start_date', 'end_date',)
