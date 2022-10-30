from django.db import models
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='todos')

    signer = Signer(sep='/', salt='todo.Todo')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        signed_pk = self.signer.sign(self.pk)
        return reverse('todo_list', args=[str(signed_pk)])

    def get_signed_pk(self):
        return self.signer.sign(self.pk)

    # returns completed jobs percent if there is
    def complete_rate(self):
        completed_jobs = self.jobs.filter(is_done=True)
        not_completed = self.jobs.filter(is_done=False)
        if self.jobs:
            return int(len(completed_jobs) * 100 / (len(completed_jobs) + len(not_completed)))
        else:
            return None


class Job(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('your job text'))
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=True, related_name='jobs')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='jobs')
    is_done = models.BooleanField(default=False)
    user_datetime = models.DateTimeField(verbose_name=_("this job's due"), blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        signed_pk = self.todo.signer.sign(self.todo.pk)
        return reverse('todo_list', args=[signed_pk])
