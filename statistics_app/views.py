from django.shortcuts import render
from todo.models import Todo, Job
from django.contrib.auth.decorators import login_required
from .statistics import Analytics
import json


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)
    analytics = Analytics(request)
    pd_count, pd_time, pd_date = analytics.get_most_productive_day_info()
    status, arrow = analytics.get_user_today_status()
    context = {"filename": 'name',
               "collapse": "",
               "labels": json.dumps(list(analytics.get_done_dates())),
               "data": json.dumps(analytics.get_job_done_each_day()),
               'todos': user_todos,
               'pd_count': pd_count,
               'pd_time': pd_time,
               'pd_date': pd_date,
               'spent_h': analytics.get_total_hours_spent(),
               'status': status,
               'arrow': arrow,
               'spent_time': json.dumps(analytics.get_daily_hour_spent()),
               'spent_today': analytics.get_today_hours_spent(),
               }
    return render(request, 'dashboard.html', context)
