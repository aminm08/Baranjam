from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Goal(models.Model):
    MEASURE_CHOICES = (
        ('t', "Today"),
        ('w', "This week"),
        ('m', "This month"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='goals')
    jobs = models.PositiveIntegerField(verbose_name=_("your done jobs count goal"))
    hours = models.PositiveIntegerField(verbose_name=_("your spent hours goal"))
    measure = models.CharField(choices=MEASURE_CHOICES, max_length=1, verbose_name=_("the measure of your goal"))

    def __str__(self):
        return f"{self.user} : {self.measure}"


