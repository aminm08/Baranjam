from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

import json

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
    success_url = reverse_lazy('homepage')
    success_message = _('successfully sent')


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)
    labels, data = [], []
    user_done_dates = [str(job.user_done_date) for job in
                       request.user.jobs.filter(is_done=True).order_by('user_done_date')]

    for date in user_done_dates:
        if date not in labels:
            labels.append(date)

    data = [user_done_dates.count(i) for i in labels]

    context = {"filename": 'name',
               "collapse": "",
               "labels": json.dumps(list(labels)),
               "data": json.dumps(data),
               'todos': user_todos
               }
    return render(request, 'dashboard.html', context)
