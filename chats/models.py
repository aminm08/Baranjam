from django.db import models
from group_lists.models import GroupList
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    group = models.ForeignKey(GroupList, on_delete=models.CASCADE, verbose_name=_('Message group'), related_name='messages')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Message sender"))
    text = models.TextField(verbose_name=_('Message text'))
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s : %s" % (self.group.title, self.user.username)


class OnlineUsers(models.Model):
    group = models.ForeignKey(GroupList, on_delete=models.CASCADE, related_name='online_users', verbose_name=_('group'))
    online_users = models.ManyToManyField(get_user_model(), verbose_name=_('Group online users'), blank=True)

    def get_online_users_length(self):
        return self.online_users.count()

    def __str__(self):
        return "%s : online users length: %s" % (self.group.title, self.get_online_users_length())
