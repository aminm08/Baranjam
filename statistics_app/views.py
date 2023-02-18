from django.shortcuts import render
from todo.models import Todo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .statistics import DashBoard
from datetime import datetime, date
import json
from .forms import DashboardApplyDateForm
from goals.forms import GoalForm


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)
    goal_form = GoalForm()
    user_goals = request.user.goals.all()

    date_apply_form = DashboardApplyDateForm(request.GET)
    if date_apply_form.is_valid():
        data_date_range = date_apply_form.cleaned_data[0]
        general_date = date_apply_form.cleaned_data[1]

        print(data_date_range, general_date)
    else:
        data_date_range = ('all',)
        general_date = date.today()

    dashboard = DashBoard(request, data_date_range, general_date)

    if not dashboard.get_done_dates_in_range():
        messages.warning(request, _('date range you entered has no data'))

    context = None

    pd_count, pd_time, pd_date = dashboard.get_most_productive_day_info()
    job_status, job_arrow, j_progress_percentage = dashboard.get_user_jobs_status()
    hours_status, hours_arrow, h_progress_percentage = dashboard.get_user_hours_spent_status()
    today_done_jobs_titles = dashboard.get_done_jobs_titles_by_general_date()
    hours_spent = dashboard.get_hours_per_job_in_general_date()
    context = {
        "goal_form": goal_form,
        "user_goals": user_goals,
        "form": date_apply_form,
        "date": general_date,
        "tasks_done_on_date": dashboard.get_tasks_done_in_general_date().count(),
        "all_tasks_done_in_range": len(dashboard.get_all_done_jobs_in_range()),
        "labels": json.dumps(dashboard.get_done_dates_in_range()),
        "data": json.dumps(dashboard.done_job_per_day()),
        'todos': user_todos,
        'pd_count': pd_count,
        'pd_time': pd_time,
        'pd_date': pd_date,
        'spent_h': dashboard.hours_all(),
        'job_status': job_status,
        'job_arrow': job_arrow,
        'job_progress_percentage': j_progress_percentage,
        'hours_status': hours_status,
        'hours_arrow': hours_arrow,
        'hours_progress_percentage': h_progress_percentage,
        'spent_time': json.dumps(dashboard.hours_per_day()),
        'spent_today': dashboard.get_general_date_hours_spend(),
        'chart_title': json.dumps(today_done_jobs_titles),
        'chart_hours': json.dumps(hours_spent),
    }

    return render(request, 'dashboard.html', context)
