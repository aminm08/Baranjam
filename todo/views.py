from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import Todo, Job


def all_user_todos(request):
    todos = Todo.objects.filter(user=request.user)

    return render(request, 'todo/user_todos.html', {'todos': todos})


@login_required()
def todo_list_main_page(request, todo_slug):
    todo = get_object_or_404(Todo, slug=todo_slug)
    user_jobs = Job.objects.filter(todo__user=request.user).order_by('is_done', '-datetime_created')

    filter = request.GET.get('filter')

    if filter == '1':
        user_jobs = Job.objects.filter(todo__user=request.user).order_by('is_done', '-datetime_created')
    elif filter == '2':
        user_jobs = Job.objects.filter(todo__user=request.user, is_done=True).order_by('is_done', '-datetime_created')
    elif filter == '3':
        user_jobs = Job.objects.filter(todo__user=request.user, is_done=False).order_by('is_done', '-datetime_created')

    # user_jobs_filter = JobFilter(request.GET, queryset=user_jobs)
    if request.method == 'POST':
        id = list(request.POST.keys())[1]
        job = get_object_or_404(Job, pk=id)
        job.is_done = True
        job.save()

    return render(request, 'todo/todo_list.html', {'user_jobs': user_jobs, 'todo': todo})


class AddTodo(generic.CreateView):
    model = Todo
    fields = ('name',)
    success_url = reverse_lazy('user_todos')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class CreateJobView(generic.CreateView):
    model = Job
    fields = ['text', 'user_datetime']

    def form_valid(self, form):
        obj = form.save(commit=False)

        todo_id = int(self.kwargs['todo_id'])
        todo = get_object_or_404(Todo, pk=todo_id)

        obj.todo = todo

        obj.save()
        return super().form_valid(form)


class JobDeleteView(generic.DeleteView):
    model = Job

    def get_success_url(self):
        return self.get_object().get_absolute_url()
