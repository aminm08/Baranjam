from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomUser(AbstractUser):
    birth_date = models.DateTimeField(verbose_name=_("your birth date"), blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, verbose_name=_('your profile picture'))
    mobile_number = models.CharField(max_length=11, verbose_name=_('your Mobile number'), blank=True)
    address = models.CharField(max_length=300, blank=True)

    def get_absolute_url(self):
        return reverse('profile')

    def get_user_completed_tasks_length(self):
        completed = self.jobs.filter(is_done=True)
        return completed
