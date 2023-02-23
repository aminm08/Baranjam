from django import forms
from datetime import date
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.utils.translation import gettext_lazy as _


class DashboardApplyDateForm(forms.Form):
    start = JalaliDateField(label=_('from'), widget=AdminJalaliDateWidget, required=False)
    end = JalaliDateField(label=_('to'), widget=AdminJalaliDateWidget, required=False)
    general_date = JalaliDateField(label=_('general date'), widget=AdminJalaliDateWidget, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date, end_date, general_date = cleaned_data.get('start'), cleaned_data.get('end'), cleaned_data.get(
            'general_date')

        # general date validation
        if general_date:
            if general_date > date.today():
                self.add_error('general_date', forms.ValidationError(_('you cannot select future date')))
        else:
            general_date = date.today()

        # validating that both fields are filled
        if start_date and not end_date:
            self.add_error('end', forms.ValidationError(_("This field is required")))

        elif end_date and not start_date:
            self.add_error('start', forms.ValidationError(_("This field is required")))

        if end_date and start_date:
            if end_date < start_date:
                self.add_error('start', error=forms.ValidationError(_("start must be less than end")))

        # no input -> show all data
        elif not start_date and not end_date:

            return [('all',), general_date]

        return [(start_date, end_date), general_date]
