from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from .utils import *
import json
from datetime import date
from .forms import ContactForm
from .models import Contact
from todo.models import Todo, Job


def homepage(request):
    return render(request, 'homepage.html')


def about_us(request):
    return render(request, 'about_us.html')


class ContactUs(SuccessMessageMixin, generic.CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_us.html'
    success_url = reverse_lazy('contact_us')
    success_message = _('successfully sent')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        obj_form = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj_form.user = self.request.user
        obj_form.ip_addr = get_client_ip_address(self.request)
        obj_form.save()
        return super().form_valid(form)


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)

    graph_dates, graph_jobs = get_done_jobs_and_their_dates(request)

    user_today_status, status_arrow = get_user_today_status(graph_jobs)
    all_spent_time = get_daily_hour_spent(request, graph_dates)

    productive_day_date, productive_day_job_count, productive_day_hours_spent = get_most_productive_day_info(graph_jobs,
                                                                                                             all_spent_time,
                                                                                                             graph_dates)

    productive_day_date = date(year=int(productive_day_date[:4]), month=int(productive_day_date[5:7]),
                               day=int(productive_day_date[8:]))
    hours, minutes = get_total_hours_spent(request)

    context = {"filename": 'name',
               "collapse": "",
               "labels": json.dumps(list(graph_dates)),
               "data": json.dumps(graph_jobs),
               'todos': user_todos,
               'pd_count': productive_day_job_count,
               'pd_time': productive_day_hours_spent,
               'pd_date': productive_day_date,
               'spent_h': hours,
               'spent_m': minutes,
               'status': user_today_status,
               'arrow': status_arrow,
               'spent_time': json.dumps(all_spent_time),
               'spent_today': all_spent_time[-1]
               }
    return render(request, 'dashboard.html', context)
