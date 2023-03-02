from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import DashboardApplyDateForm
from .statistics import DashBoard
from goals.forms import GoalForm

from datetime import datetime, date
from jalali_date import date2jalali
import json


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
    goal_form = GoalForm()
    user_goals = request.user.goals.all()
    apply_date_form = DashboardApplyDateForm(request.GET)
    dashboard = get_dashboard_obj(request, apply_date_form)

    if not dashboard.get_done_dates_in_range():
        messages.warning(request, _('date range you entered has no data'))
    context = {
        "goal_form": goal_form,
        "apply_date_form": apply_date_form,
        "user_goals": user_goals,
        "general_date": date2jalali(dashboard.general_date),
        "tasks_done_in_general_date": dashboard.get_tasks_done_in_general_date().count(),
        "all_tasks_done_in_range": dashboard.get_done_jobs_in_range().count(),
        'todos': request.user.todos.all(),
        'total_hours_spent': dashboard.get_total_hours_spent(),
        'hours_spent_in_general_date': dashboard.get_general_date_hours_spent(),

    }
    if dashboard.all_done_jobs:
        context = {
            # charts
            "jalali_done_dates_in_range": json.dumps(
                dashboard.convert_done_dates_to_jalali_date(dashboard.get_done_dates_in_range())),
            "done_jobs_count_per_day_in_range": json.dumps(
                dashboard.get_done_jobs_count_per_day(dashboard.get_done_dates_in_range())),
            'general_date_done_jobs_titles': json.dumps(dashboard.get_done_jobs_titles_by_general_date()),
            'general_date_hours_spent_per_job': json.dumps(dashboard.get_hours_per_job_in_general_date()),
            'spent_time': json.dumps(dashboard.get_hours_spent_per_day(dashboard.get_done_dates_in_range())),

            "goal_form": goal_form,
            "apply_date_form": apply_date_form,
            "goals_progress": json.dumps(dashboard.get_goal_progress_percentage()),
            "user_goals": user_goals,
            "general_date": date2jalali(dashboard.general_date),
            "tasks_done_in_general_date": dashboard.get_tasks_done_in_general_date().count(),
            "all_tasks_done_in_range": dashboard.get_done_jobs_in_range().count(),
            'todos': request.user.todos.all(),
            'most_productive_day_info': dashboard.get_most_productive_day_info(),
            'total_hours_spent': dashboard.get_total_hours_spent(),
            'job_status': dashboard.get_user_jobs_status(),
            'hour_status': dashboard.get_user_hours_spent_status(),
            'hours_spent_in_general_date': dashboard.get_general_date_hours_spent(),
        }

    return render(request, 'dashboard.html', context)
