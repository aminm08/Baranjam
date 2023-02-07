from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.signing import Signer
from django.utils.text import slugify
from django.contrib.sites.models import Site


class GroupList(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Group title'))
    todo = models.ManyToManyField('todo.Todo', related_name='group_todos')
    members = models.ManyToManyField(get_user_model(), related_name='as_member', verbose_name=_('member users'))
    admins = models.ManyToManyField(get_user_model(), related_name='as_admin', verbose_name=_('Group admins'))
    description = models.TextField(verbose_name=_('group description'), null=True, blank=True)
    picture = models.ImageField(verbose_name=_('group Picture'), upload_to='group_pics/', null=True, blank=True)
    enable_chat = models.BooleanField(default=True, verbose_name=_('Group members chat'))
    enable_job_divider = models.BooleanField(default=False, verbose_name=_('Group job divider'))
    InvLink = Signer(sep='/', salt='group_lists.GroupList')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(GroupList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('group_detail', args=[self.pk])

    def get_all_members_length(self):
        return len(self.members.all()) + len(self.admins.all())

    def get_all_members_obj(self):
        return [*self.admins.all(), *self.members.all()]

    def get_invitation_link(self):
        return 'https://%s/%s' % ('127.0.0.1:8000', self.InvLink.sign(self.pk))
