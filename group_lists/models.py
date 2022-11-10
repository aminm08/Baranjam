from django.db import models
from django.contrib.auth import get_user_model


class GroupList(models.Model):
    todo = models.ForeignKey('todo.Todo', on_delete=models.CASCADE, related_name='group_todo')
    users = models.ManyToManyField(get_user_model(), related_name='group_users')
