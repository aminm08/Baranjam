from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count
from datetime import date
from .forms import JobForm, TodoForm
from .models import Todo, Job


@login_required()
def all_user_todos(request):
    todos = Todo.objects.filter(user=request.user).annotate(Count('jobs')).order_by('-jobs__count')
    return render(request, 'todo/user_todos.html', {'todos': todos})


@login_required()
@require_POST
def todo_apply_options_post_view(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.user:
        option_number = str(request.POST.get('action'))

        match option_number:
            case '1':
                todo.jobs.all().delete()
                messages.success(request, _('todo list successfully cleared'))

            case '2':
                finished_jobs = todo.get_jobs()
                finished_jobs.delete()
                messages.success(request, _('finished jobs has deleted successfully'))

            case '3':
                finished_jobs = todo.get_jobs()
                for job in finished_jobs:
                    job.is_done = False
                    job.user_done_date = None
                    job.save()
                messages.success(request, _('all jobs are now active'))

            case '4':
                unfinished_jobs = todo.get_jobs(finished=False)
                for job in unfinished_jobs:
                    job.is_done = True
                    job.user_done_date = date.today()
                    job.save()
                messages.success(request, _('all jobs are now checked'))
        return redirect(todo.get_absolute_url())

    raise PermissionDenied


@login_required()
def todo_list_main_page(request, signed_pk):
    todo = get_object_or_404(Todo, pk=Todo.signer.unsign(signed_pk))

    if request.user == todo.user or todo.user_from_group_has_permission(request.user):

        user_undone_jobs = todo.jobs.filter(is_done=False).order_by('user_date', '-datetime_created')
        user_done_jobs = todo.jobs.filter(is_done=True).order_by('-user_done_date')
        user_filter = str(request.GET.get('filter'))

        match user_filter:
            case 'all':
                user_undone_jobs = todo.jobs.filter(is_done=False).order_by('user_date', '-datetime_created')
                user_done_jobs = todo.jobs.filter(is_done=True).order_by('-user_done_date')
            case 'actives':
                user_undone_jobs = todo.jobs.filter(is_done=False).order_by('user_date', '-datetime_created')
                user_done_jobs = []
            case 'done':
                user_done_jobs = todo.jobs.filter(is_done=True).order_by('-user_done_date')
                user_undone_jobs = []

        return render(request, 'todo/todo_list.html',
                      {'user_jobs': [*user_undone_jobs, *user_done_jobs], 'todo': todo, 'form': JobForm()})

    raise PermissionDenied


@login_required()
@require_POST
def job_set_is_done_status(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.todo.user == request.user:

        if not job.is_done:
            job.is_done = True
            job.user_done_date = date.today()
            messages.success(request, _('job completed! congrats'))

        else:
            job.is_done = False
            job.user_done_date = None
        job.save()
        return redirect(job.todo.get_absolute_url())
    raise PermissionDenied


@login_required()
def job_update_view(request, signed_pk, job_id):
    todo = get_object_or_404(Todo, pk=Todo.signer.unsign(signed_pk))
    if todo.user == request.user:

        job = get_object_or_404(Job, pk=job_id)
        form = JobForm(instance=job)

        if request.method == 'POST':
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                job_obj = form.save(commit=False)
                job_obj.user = request.user
                job_obj.todo = todo

                job_obj.save()
                messages.success(request, _('your job updated successfully'))
                return redirect(todo.get_absolute_url())

        return render(request, 'todo/update_job.html', {'form': form, 'todo': todo, 'job': job})
    raise PermissionDenied


class AddTodo(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Todo
    http_method_names = ['post']
    form_class = TodoForm
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

    def get_todo_from_kwargs(self):
        todo_id = int(self.kwargs['todo_id'])
        todo = get_object_or_404(Todo, pk=todo_id)
        return todo

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.todo = self.get_todo_from_kwargs()
        obj.user = self.request.user

        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect(self.get_todo_from_kwargs().get_absolute_url())

    def test_func(self):
        return self.request.user == self.get_todo_from_kwargs().user


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Job
    success_message = _('Task successfully deleted of your list')
    http_method_names = ['post']

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().todo.user


def todo_delete_view(request, signed_pk):
    todo = get_object_or_404(Todo, pk=Todo.signer.unsign(signed_pk))
    if todo.user == request.user:
        if request.method == 'POST':
            todo.delete()
            messages.success(request, _("todo list successfully deleted"))
            return redirect('user_todos')
        return render(request, 'todo/todo_delete.html', {'todo': todo})
    raise PermissionDenied


@login_required()
def todo_list_settings(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.user:
        return render(request, 'todo/todo_settings.html', {'todo': todo})
    raise PermissionDenied


@login_required()
@require_POST
def todo_update_list_name(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.user:
        new_name = str(request.POST['name'])
        todo.name = new_name
        todo.save()
        messages.success(request, _('your list name successfully updated'))
        return redirect('todo_settings', todo.id)
    raise PermissionDenied
