from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.urls import reverse


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, verbose_name=_('your profile picture'))
    all_jobs_done = models.PositiveIntegerField(verbose_name=_('all jobs done'), default=0)

    def get_absolute_url(self):
        return reverse('profile')

    def update_done_jobs(self, add=True):
        if add:
            self.all_jobs_done += 1
        elif self.all_jobs_done != 0:
            self.all_jobs_done -= 1

        self.save()

    def get_user_today_completed_tasks(self):
        completed = self.jobs.filter(user_done_date=date.today(), is_done=True)
        return completed

    # def get_joined_groups(self):
    #     print(self.group)
