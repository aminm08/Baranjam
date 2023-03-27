from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DashboardApplyDateForm
from .statistics import DashBoard, get_context_data
from datetime import datetime, date


@login_required
def dashboard_view(request):
    apply_date_form = DashboardApplyDateForm(request.GET)
    context = get_context_data(request, apply_date_form)
    return render(request, 'dashboard.html', context)
