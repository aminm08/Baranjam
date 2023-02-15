from django.shortcuts import render
from todo.models import Todo, Job
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from .statistics import DashBoard
from datetime import datetime
import json


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)
    date_range = request.GET.get('range').split() if request.GET.get('range') else ["all"]

    dashboard = DashBoard(request, date_range)

    if not dashboard.validate_range(date_range):
        messages.warning(request, _('Invalid date range'))
        return redirect('dashboard')

    context = None
    if dashboard.all_done_jobs:
        pd_count, pd_time, pd_date = dashboard.get_most_productive_day_info()
        status, arrow = dashboard.get_user_today_status()
        today_done_jobs_titles = dashboard.get_today_done_jobs_title()
        hours_spent = dashboard.hours_per_job()
        context = {
            "labels": json.dumps(dashboard.get_done_dates()),
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
    print(context)
    return render(request, 'dashboard.html', context)
