from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Message(models.Model):
    msg_text = models.CharField(max_length=200, blank=False)
    send_time = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, related_name='sender_user', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name='reciever_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.msg_text[:10]

    @classmethod
    def create(cls, msg_text, sender, reciever):
        message = cls(msg_text=msg_text, sender=sender, reciever=reciever)
        return message


class Group(models.Model):
    group_name = models.CharField(max_length=20)
    members = models.ManyToManyField(User, related_name='group_members')


class GroupMessage(models.Model):
    message_text = models.CharField(max_length=200)
    send_time = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='related_group', on_delete=models.CASCADE)
