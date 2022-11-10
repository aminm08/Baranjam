from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GroupList
from pages.models import Invitation
model = GroupList


# @receiver(post_save, sender=model)
# def my_callback(sender, instance, created, **kwargs):
#     if created:
#         inv = Invitation.objects.create(user_receiver=instance.user)
#
