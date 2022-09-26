from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Job
from .forms import JobFilter


@login_required()
def todo_main_page(request):
    user = get_object_or_404(get_user_model(), pk=request.user.id)
    user_jobs = Job.objects.filter(user=user).order_by('is_done', '-datetime_created')

    filter = request.GET.get('filter')

    if filter == '1':
        user_jobs = Job.objects.filter(user=user).order_by('is_done', '-datetime_created')
    elif filter == '2':
        user_jobs = Job.objects.filter(user=user, is_done=True).order_by('is_done', '-datetime_created')
    elif filter == '3':
        user_jobs = Job.objects.filter(user=user, is_done=False).order_by('is_done', '-datetime_created')



    # user_jobs_filter = JobFilter(request.GET, queryset=user_jobs)
    if request.method == 'POST':
        id = list(request.POST.keys())[1]
        job = get_object_or_404(Job, pk=id)
        job.is_done = True
        job.save()

    return render(request, 'jobs/todo_list.html', {'user_jobs': user_jobs, })


class CreateJobView(generic.CreateView):
    model = Job
    fields = ['text', 'user_datetime']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        obj.save()
        return super().form_valid(form)


class JobDeleteView(generic.DeleteView):
    model = Job
    success_url = reverse_lazy('todo_list')
