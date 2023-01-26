from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.http import Http404
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
    group_list_users = todo.group_todo.last().users.all() if todo.is_group_list() else []

    if request.user == todo.user or request.user in group_list_users:

        user_jobs = Job.objects.filter(todo=todo).order_by('is_done', '-user_date')
        user_filter = str(request.GET.get('filter'))

        match user_filter:
            case 'all':
                user_jobs = request.user.jobs.filter(todo=todo).order_by('is_done', '-datetime_created')
            case 'actives':
                user_jobs = request.user.jobs.filter(todo=todo, is_done=False).order_by('-datetime_created')
            case 'done':
                user_jobs = request.user.jobs.filter(todo=todo, is_done=True).order_by('-datetime_created')

        return render(request, 'todo/todo_list.html', {'user_jobs': user_jobs, 'todo': todo, 'form': JobForm()})

    raise PermissionDenied


@login_required()
@require_POST
def job_is_done_assign(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.todo.user == request.user:

        if not job.is_done:
            job.is_done = True
            job.user_done_date = date.today()  # for statistics
            request.user.update_done_jobs()
            messages.success(request, _('job completed! congrats'))


        else:
            job.is_done = False
            job.user_done_date = None
            request.user.update_done_jobs(add=False)
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
                return redirect('job_update', todo.get_signed_pk(), job.id)

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
        messages.error(self.request, _('invalid field value'))
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


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Todo
    template_name = 'todo/todo_delete.html'
    context_object_name = 'todo'
    success_url = reverse_lazy('user_todos')
    success_message = _('todo list successfully deleted')

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        signed_pk = self.kwargs.get('signed_pk')
        if signed_pk:
            try:
                todo_obj = get_object_or_404(self.model, pk=self.model.signer.unsign(signed_pk))
            except:
                raise Http404

            return todo_obj
        raise AttributeError(
            "Generic Detail view %s must be called"
            "with signed pk in the URLconf" % self.__class__.__name__)


@login_required()
def todo_list_detail_and_settings(request, pk):
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


