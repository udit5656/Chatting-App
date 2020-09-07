from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
from django.db.models import Q


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


class Chat(models.Model):
    latest_message = models.ForeignKey(Message, related_name='latest_message', on_delete=models.CASCADE)
    member_one = models.ForeignKey(User, related_name='member_one', on_delete=models.CASCADE)
    member_two = models.ForeignKey(User, related_name='member_two', on_delete=models.CASCADE)

    def __str__(self):
        return self.member_one.username

    def get_other_member(self, member):
        if self.member_one == member:
            return self.member_two
        else:
            return self.member_one

    def delete_latest_message(self):
        messages = Message.objects.filter((Q(sender=self.member_one) | Q(sender=self.member_two)),
                                          (Q(reciever=self.member_two) | Q(reciever=self.member_one))).order_by(
            '-send_time')
        if messages.count() > 1:
            updated_latest_message = messages[1]
            updated_chat = Chat.create(latest_message=updated_latest_message, member_one=self.member_one,
                                       member_two=self.member_two)
            updated_chat.save()
            self.delete()
        else:
            self.delete()

    @classmethod
    def create(cls, latest_message, member_one, member_two):
        chat = cls(latest_message=latest_message, member_one=member_one, member_two=member_two)
        return chat

    def update_latest_message(self, message):
        chat = Chat.create(latest_message=message, member_one=self.member_one, member_two=self.member_two)
        chat.save()
        self.delete()


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
