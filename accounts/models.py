from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.urls import reverse


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, verbose_name=_('your profile picture'))

    def get_absolute_url(self):
        return reverse('profile')

    def get_user_all_jobs_done(self):
        all_jobs_done = self.jobs.filter(is_done=True)
        return all_jobs_done

    def get_user_today_completed_tasks(self):
        completed = self.jobs.filter(user_done_date=date.today(), is_done=True)
        return completed
