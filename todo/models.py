from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    slug = models.SlugField(null=True, unique=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('todo_list', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Job(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('your job text'))
    todo = models.ForeignKey('todo.Todo', on_delete=models.CASCADE, null=True)
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    user_datetime = models.DateTimeField(verbose_name=_("this job's due"), blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('todo_list', args=[self.todo.slug])
