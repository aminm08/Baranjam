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

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.group_todo.all().delete()
        super(Todo, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        signed_pk = self.get_signed_pk()
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

    def get_jobs(self, finished=True):
        return self.jobs.all().filter(is_done=finished)

    def is_group_list(self):
        return self.group_todo.exists()


class Job(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('your job text'),
                            error_messages={'required': _('Please enter job text')})
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=True, related_name='jobs')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='jobs')
    duration = models.TimeField(verbose_name=_('job duration'), blank=True, null=True)
    is_done = models.BooleanField(default=False, verbose_name=_('job is done'))

    user_date = models.DateField(verbose_name=_('job date'), blank=True, null=True, )
    user_time = models.TimeField(verbose_name=_('job time'), blank=True, null=True)
    user_done_date = models.DateField(null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        signed_pk = self.todo.signer.sign(self.todo.pk)
        return reverse('todo_list', args=[signed_pk])

    def get_duration(self):
        if self.duration.hour and self.duration.minute:
            return '%d hours, %d minutes' % (self.duration.hour, self.duration.minute)
        elif self.duration.hour and not self.duration.minute:
            return '%d hours ' % self.duration.hour
        else:
            return '%d minutes' % self.duration.minute
