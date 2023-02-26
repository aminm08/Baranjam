from django.db import models
from django.contrib.auth import get_user_model
from group_lists.models import GroupList
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Contact(models.Model):
    full_name = models.CharField(max_length=100, verbose_name=_('your Full Name'))
    email = models.EmailField(verbose_name=_('your Email'))
    phone_regex = RegexValidator(regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
                                 message=_("Invalid phone number"))
    phone_number = models.CharField(validators=[phone_regex], max_length=17, verbose_name=_('your phone number'))
    message = models.TextField(verbose_name=_('your Message'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('user'))
    ip_addr = models.GenericIPAddressField(verbose_name=_('user ip address'), null=True)

    def __str__(self):
        return self.full_name


