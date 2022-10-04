from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import json
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from webpush import send_user_notification

from .forms import JobForm
from .models import Todo, Job


@login_required()
def all_user_todos(request):
    todos = Todo.objects.filter(user=request.user).order_by('-datetime_created')

    return render(request, 'todo/user_todos.html', {'todos': todos})


@login_required()
def todo_list_main_page(request, signed_pk):
    pk = Todo.signer.unsign(signed_pk)
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.user:

        user_jobs = request.user.jobs.filter(todo=todo).order_by('is_done', '-datetime_created')

        user_filter = request.GET.get('filter')

        if user_filter == '1':
            user_jobs = request.user.jobs.filter(todo=todo).order_by('is_done', '-datetime_created')

        elif user_filter == '2':
            user_jobs = request.user.jobs.filter(todo=todo, is_done=True).order_by('is_done', '-datetime_created')

        elif user_filter == '3':
            user_jobs = request.user.jobs.filter(todo=todo, is_done=False).order_by('is_done', '-datetime_created')

        if request.method == 'POST':

            id = list(request.POST.keys())[1]
            job = get_object_or_404(Job, pk=id)

            if not job.is_done:
                job.is_done = True
                messages.success(request, _('job completed! congrats'))
            else:
                job.is_done = False
            job.save()

        return render(request, 'todo/todo_list.html', {'user_jobs': user_jobs, 'todo': todo, 'form': JobForm()})
    else:
        raise PermissionDenied


class AddTodo(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Todo
    fields = ('name',)
    success_url = reverse_lazy('user_todos')
    success_message = _('Todo list successfully created')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class CreateJobView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    model = Job
    form_class = JobForm
    success_message = _('Task successfully added to your list')

    def form_valid(self, form):
        obj = form.save(commit=False)

        todo_id = int(self.kwargs['todo_id'])
        todo = get_object_or_404(Todo, pk=todo_id)

        obj.todo = todo
        obj.user = self.request.user

        obj.save()
        return super().form_valid(form)

    def test_func(self):
        todo = get_object_or_404(Todo, pk=int(self.kwargs['todo_id']))
        return self.request.user == todo.user


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Job
    success_message = _('Task successfully deleted of your list')

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().todo.user


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Todo
    success_url = reverse_lazy('user_todos')
    success_message = _('todo list successfully deleted')

    def test_func(self):
        return self.request.user == self.get_object().user


def render_pdf(request, todo_id):
    # pulling todo and its jobs
    todo = get_object_or_404(Todo, pk=todo_id)
    jobs = todo.jobs.filter(user=request.user)

    buf = io.BytesIO()

    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont('Helvetica', 14)

    data = [i.text for i in jobs]

    for d in data:
        text_obj.textLine(d)

    # write the document to disk
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='out.pdf')

