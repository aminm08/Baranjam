from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from todo.models import Todo


class Habit(models.Model):
    REPETITIVENESS_CHOICES = (
        ('e', _('Everyday')),
        ('w', _('Specific days in week')),
        ('m', _('Specific days in month')),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(_('Habit title'), max_length=100)
    todo_list = models.ForeignKey(Todo, on_delete=models.CASCADE, verbose_name=_('Habit To-do list'))
    description = models.TextField(_('Habit description'), max_length=300)
    repetitiveness = models.CharField(_('Habit repetitiveness'), choices=REPETITIVENESS_CHOICES, max_length=1)
    start_date = models.DateField(verbose_name=_('Habit start date'), default=timezone.now)
    end_date = models.DateField(verbose_name=_('Habit end date'), blank=True, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} : {self.get_repetitiveness_display()}'
