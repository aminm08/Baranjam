from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.signing import Signer
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
import uuid


class GroupList(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200, verbose_name=_('Group title'))
    todo = models.ManyToManyField('todo.Todo', related_name='group_todos')
    members = models.ManyToManyField(get_user_model(), related_name='group_lists_as_member',verbose_name=_('member users'),blank=True)
    admins = models.ManyToManyField(get_user_model(), related_name='group_lists_as_admin',verbose_name=_('Group admins'),blank=True)
    description = models.TextField(verbose_name=_('group description'), null=True, blank=True)
    picture = models.ImageField(verbose_name=_('group Picture'), upload_to='group_pics/', null=True, blank=True)
    enable_chat = models.BooleanField(default=True, verbose_name=_('Group members chat'))
    enable_job_divider = models.BooleanField(default=False, verbose_name=_('Group job divider'))
    InvLink = Signer(sep='/', salt='group_lists.GroupList')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group_detail', args=[self.pk])

    def get_all_members_length(self):
        return len(self.members.all()) + len(self.admins.all())

    def get_group_picture_or_blank(self):
        return self.picture.url if self.picture else '/static/img/blank_user.png'

    def get_all_members_obj(self):
        return [*self.admins.all(), *self.members.all()]

    def get_signed_pk(self):
        return self.InvLink.sign(self.pk)

    def get_invitation_link(self):
        url = reverse('foreign_inv_show_info', args=[self.get_signed_pk()])
        return 'http://%s%s' % ('127.0.0.1:8000', url)

    def picture_preview(self):
        return mark_safe(f'<img src={self.get_group_picture_or_blank()} width=60 height=60> </img>')
