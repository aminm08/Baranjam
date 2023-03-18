from django.db import models
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import date


class Todo(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Todo-list name"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='todos',
                             verbose_name=_("Todo-list owner"))
    signer = Signer(sep='/', salt='todo.Todo')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        signed_pk = self.get_signed_pk()
        return reverse('todo_list', args=[str(signed_pk)])

    def get_signed_pk(self):
        return self.signer.sign(self.pk)

    def complete_rate_percentage(self):
        completed_jobs = self.jobs.filter(is_done=True)
        not_completed_jobs = self.jobs.filter(is_done=False)
        if completed_jobs:
            return int(len(completed_jobs) * 100 / (len(completed_jobs) + len(not_completed_jobs)))
        else:
            return None

    def get_finished_jobs(self):
        return self.jobs.all().filter(is_done=True)

    def get_unfinished_jobs(self):
        return self.jobs.all().filter(is_done=False)

    def user_from_group_has_permission(self, user):
        for group in self.group_todos.all():
            if group.is_in_group(user):
                return True
        return False

    def is_owner(self, user):
        return self.user == user

    def is_group_list(self):
        return self.group_todos.exists()

    def delete_all_jobs(self):
        self.jobs.all().delete()

    def active_all_jobs(self):
        for job in self.get_finished_jobs():
            job.is_done = False
            job.user_done_date = None
            job.save()

    def check_all_jobs(self):
        for job in self.get_unfinished_jobs():
            job.is_done = True
            job.user_done_date = date.today()
            job.save()

    def get_user_jobs_by_filter(self, filter: str):
        user_undone_jobs = self.jobs.filter(is_done=False).order_by('user_date', '-datetime_created')
        user_done_jobs = self.jobs.filter(is_done=True).order_by('-user_done_date')
        if filter == 'actives':
            user_done_jobs = []
        elif filter == 'done':
            user_undone_jobs = []
        return [*user_undone_jobs, *user_done_jobs]


class Job(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('your job text'))
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=True, related_name='jobs')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='jobs')
    duration = models.TimeField(verbose_name=_('job duration'), blank=True, null=True)
    is_done = models.BooleanField(default=False, verbose_name=_('job is done'))
    notes = models.TextField(null=True, blank=True, verbose_name=_('job notes'))

    user_date = models.DateField(verbose_name=_('job date'), blank=True, null=True)
    user_done_date = models.DateField(null=True, blank=True, verbose_name=_("done date"))
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        signed_pk = self.todo.signer.sign(self.todo.pk)
        return reverse('todo_list', args=[signed_pk])

    def get_duration(self):

        if self.duration.hour and self.duration.minute:
            return '%dh, %dm' % (self.duration.hour, self.duration.minute)
        elif self.duration.hour and not self.duration.minute:
            return '%dh ' % self.duration.hour
        else:
            return '%dm ' % self.duration.minute
