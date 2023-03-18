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
from .decorators import list_owner_only
from .models import Todo, Job


@login_required()
def all_user_todos(request):
    todos = Todo.objects.filter(user=request.user).annotate(Count('jobs')).order_by('-jobs__count')
    return render(request, 'todo/user_todos.html', {'todos': todos})


@login_required()
@require_POST
@list_owner_only
def todo_apply_options_view(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    option_number = str(request.POST.get('action'))

    if option_number == '1':
        todo.delete_all_jobs()
        messages.success(request, _('todo list successfully cleared'))
    elif option_number == '2':
        finished_jobs = todo.get_finished_jobs()
        finished_jobs.delete()
        messages.success(request, _('finished jobs has deleted successfully'))
    elif option_number == '3':
        todo.active_all_jobs()
        messages.success(request, _('all jobs are now active'))

    elif option_number == '4':
        todo.check_all_jobs()
        messages.success(request, _('all jobs are now checked'))
    return redirect(todo.get_absolute_url())


@login_required()
def todo_list_main_page(request, signed_pk):
    todo = get_object_or_404(Todo, pk=Todo.signer.unsign(signed_pk))

    if request.user == todo.user or todo.user_from_group_has_permission(request.user):
        user_filter = str(request.GET.get('filter'))
        user_jobs = todo.get_user_jobs_by_filter(user_filter)

        return render(request, 'todo/todo_list.html', {'user_jobs': user_jobs, 'todo': todo, 'form': JobForm()})

    raise PermissionDenied


@login_required()
@require_POST
def job_set_is_done_status(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.todo.user == request.user:
        if job.is_done:
            job.is_done = False
            job.user_done_date = None

        else:
            job.is_done = True
            job.user_done_date = date.today()
            messages.success(request, _('job completed! congrats'))
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
    success_message = _('Task successfully deleted from your list')
    http_method_names = ['post']

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().todo.user


@login_required()
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
@list_owner_only
def todo_list_settings(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    return render(request, 'todo/todo_settings.html', {'todo': todo})


@login_required()
@require_POST
@list_owner_only
def todo_update_list_name(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    new_name = str(request.POST['name'])
    todo.name = new_name
    todo.save()
    messages.success(request, _('your list name successfully updated'))
    return redirect('todo_settings', todo.id)
