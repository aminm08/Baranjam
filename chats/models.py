from django.db import models
from group_lists.models import GroupList
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    group = models.ForeignKey(GroupList, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Message text'))
    datetime_created = models.DateTimeField(auto_now_add=True)


class OnlineUsers(models.Model):
    group = models.ForeignKey(GroupList, on_delete=models.CASCADE, related_name='online_users')
    online_users = models.ManyToManyField(get_user_model())

