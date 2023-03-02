from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField
from datetime import date


class Goal(models.Model):
    MEASURE_CHOICES = (
        ('d', "Daily"),
        ('w', "This week"),
        ('m', "This month"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='goals')
    jobs = models.PositiveIntegerField(verbose_name=_("your done jobs count goal"))
    hours = models.PositiveIntegerField(verbose_name=_("your spent hours goal"))
    measure = models.CharField(choices=MEASURE_CHOICES, max_length=1, verbose_name=_("the measure of your goal"))

    def __str__(self):
        return f"{self.user} : {self.measure}"

    def get_jobs_progress(self):
        progress_percentage = 0
        if self.measure == 'd':
            current_jobs_count = self.user.jobs.filter(is_done=True, user_done_date=date.today()).count()
            progress_percentage = current_jobs_count / self.jobs * 100
        print(progress_percentage)
        return progress_percentage

    def get_hours_progress(self):
        progress_percentage = 0
        if self.measure == 'd':
            hours = [job.duration.hour + job.duration.minute / 60 for
                     job in self.user.jobs.filter(is_done=True, user_done_date=date.today())
                     if job.duration]
            current_hours_count = sum(hours)
            progress_percentage = current_hours_count / self.hours * 100
        return progress_percentage
