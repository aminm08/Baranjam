from django.db import models
from django.contrib.auth import get_user_model
from group_lists.models import GroupList


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    message = models.TextField()

    def __str__(self):
        return self.full_name


class Invitation(models.Model):
    user_sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sender')
    user_receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='receiver')
    group_list = models.ForeignKey(GroupList, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_sender}->{self.user_receiver}'
