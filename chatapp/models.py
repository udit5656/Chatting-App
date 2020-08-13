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
    group_name = models.CharField(max_length=20, unique=True)
    members = models.ManyToManyField(User, related_name='group_members')
    group_code = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

    @classmethod
    def create(cls, group_name, group_code):
        group = cls(group_name=group_name, group_code=group_code)
        return group


class GroupMessage(models.Model):
    message_text = models.CharField(max_length=200)
    send_time = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='related_group', on_delete=models.CASCADE)

    def __str__(self):
        return self.message_text[:10]

    @classmethod
    def create(cls, message_text, sender, group):
        message = cls(message_text=message_text, sender=sender, group=group)
        return message
