from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class GroupList(models.Model):
    # title = models.CharField(max_length=200, verbose_name=_('Group title'))
    todo = models.ForeignKey('todo.Todo', on_delete=models.CASCADE, related_name='group_todo')
    users = models.ManyToManyField(get_user_model(), related_name='group_users', verbose_name=_('member users'))
