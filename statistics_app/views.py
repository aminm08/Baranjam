from django.shortcuts import render
from todo.models import Todo, Job
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from .statistics import DashBoard
from datetime import datetime, date
import json
from .forms import DateRangeForm


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)
    data_date_range = None

    form = DateRangeForm(request.GET)

    if form.is_valid():
        data_date_range = form.cleaned_data
    else:
        data_date_range = ['all']
    general_date = request.GET.get('date') or date.today()
    if datetime.strptime(general_date, '%Y-%m-%d') > datetime.today():
        messages.warning(request, _('you cannot select future date'))

    dashboard = DashBoard(request, data_date_range, general_date)

    if not dashboard.get_done_dates_in_range():
        messages.warning(request, _('date range you entered has no data'))

    context = None
    if dashboard.all_done_jobs:
        pd_count, pd_time, pd_date = dashboard.get_most_productive_day_info()
        status, arrow = dashboard.get_user_today_status()
        today_done_jobs_titles = dashboard.get_today_done_jobs_title()
        hours_spent = dashboard.hours_per_job()
        context = {
            "date": general_date,
            "form": form,
            "tasks_done_on_date": dashboard.get_tasks_done().count(),
            "labels": json.dumps(dashboard.get_done_dates_in_range()),
            "data": json.dumps(dashboard.done_job_per_day()),
            'todos': user_todos,
            'pd_count': pd_count,
            'pd_time': pd_time,
            'pd_date': pd_date,
            'spent_h': dashboard.hours_all(),
            'status': status,
            'arrow': arrow,
            'spent_time': json.dumps(dashboard.hours_per_day()),
            'spent_today': dashboard.hours_today(),
            'chart_title': json.dumps(today_done_jobs_titles),
            'chart_hours': json.dumps(hours_spent),
        }

    return render(request, 'dashboard.html', context)
