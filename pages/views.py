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
import math, numpy


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
    labels, data = get_done_jobs_by_date(request)
    status, arrow = get_status(data)
    pd = get_max(data)
    productive_day_job_count = data[pd]
    str_date = labels[pd]
    productive_day_date = date(year=int(str_date[:4]), month=int(str_date[5:7]), day=int(str_date[8:]))

    h, m = get_total_hours_spent(request)

    context = {"filename": 'name',
               "collapse": "",
               "labels": json.dumps(list(labels)),
               "data": json.dumps(data),
               'todos': user_todos,
               'pd_count': productive_day_job_count,
               'pd_date': productive_day_date,
               'spent_h': h,
               'spent_m': m,
               'status': status,
               'arrow': arrow,
               }
    return render(request, 'dashboard.html', context)
