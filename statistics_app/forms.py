from django import forms
from datetime import datetime
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class DateRangeForm(forms.Form):
    start = JalaliDateField(label='from', widget=AdminJalaliDateWidget, required=False)
    end = JalaliDateField(label='to', widget=AdminJalaliDateWidget, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date, end_date = cleaned_data.get('start'), cleaned_data.get('end')

        # validating that both fields are filled
        if start_date and not end_date:
            self.add_error('end', forms.ValidationError("This field is required"))

        elif end_date and not start_date:
            self.add_error('start', forms.ValidationError("This field is required"))

        if end_date and start_date:
            if end_date < start_date:
                self.add_error('start', error=forms.ValidationError("start must be less than end"))

        # no input -> show all data
        elif not start_date and not end_date:

            return ['all']

        return [start_date, end_date]
