from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DashboardApplyDateForm
from .statistics import DashBoard, get_context_data
from datetime import datetime, date


def get_dashboard_obj(request, form):
    if form.is_valid():
        data_date_range = form.cleaned_data[0]
        general_date = form.cleaned_data[1]
    else:
        data_date_range = ('all',)
        general_date = date.today()

    return DashBoard(request, data_date_range, general_date)


@login_required
def dashboard_view(request):
    apply_date_form = DashboardApplyDateForm(request.GET)
    context = get_context_data(request, apply_date_form)
    return render(request, 'dashboard.html', context)
