from django.db import models
from django.contrib.auth import get_user_model
from group_lists.models import GroupList
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    full_name = models.CharField(max_length=100, verbose_name=_('your Full Name'))
    email = models.EmailField(verbose_name=_('your Email'))
    phone_number = models.CharField(max_length=11, verbose_name=_('your Phone Number'))
    message = models.TextField(verbose_name=_('your Message'))

    def __str__(self):
        return self.full_name


class Invitation(models.Model):
    user_sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sender',
                                    verbose_name=_('the sender user'))
    user_receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='receiver',
                                      verbose_name=_('the receiver user'))
    group_list = models.ForeignKey(GroupList, on_delete=models.CASCADE, related_name='invitations',
                                   verbose_name=_('group list'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('date time created'))

    def __str__(self):
        return f'{self.user_sender}->{self.user_receiver}'
