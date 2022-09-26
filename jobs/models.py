from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('your job text'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    user_datetime = models.DateTimeField(verbose_name=_("this job's due"), blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('todo_list')



