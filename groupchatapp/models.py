from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    members = models.ManyToManyField(User, related_name='group_members')
    group_code = models.CharField(max_length=100)
    max_group_size = models.IntegerField(default=5)
    admin = models.CharField(default='uditg', max_length=50)

    def __str__(self):
        return self.group_name

    @classmethod
    def create(cls, group_name, group_code, admin):
        group = cls(group_name=group_name, group_code=group_code, admin=admin)
        return group

    def check_for_vacancy(self):
        if self.members.all().count() < self.max_group_size:
            return True
        else:
            return False


class GroupMessage(models.Model):
    message_text = models.CharField(max_length=500)
    send_time = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='related_group', on_delete=models.CASCADE)

    def __str__(self):
        return self.message_text[:10]

    @classmethod
    def create(cls, message_text, sender, group):
        message = cls(message_text=message_text, sender=sender, group=group)
        return message
