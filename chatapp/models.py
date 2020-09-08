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
    unread = models.BooleanField(default=True)

    def __str__(self):
        if len(self.msg_text) <= 30:
            return self.msg_text[:30]
        return self.msg_text[:30] + "..."

    @classmethod
    def create(cls, msg_text, sender, reciever):
        message = cls(msg_text=msg_text, sender=sender, reciever=reciever, unread=True)
        return message


class Chat(models.Model):
    latest_message = models.ForeignKey(Message, related_name='latest_message', on_delete=models.CASCADE)
    member_one = models.ForeignKey(User, related_name='member_one', on_delete=models.CASCADE)
    member_two = models.ForeignKey(User, related_name='member_two', on_delete=models.CASCADE)
    last_message_time = models.DateTimeField(default=datetime.now)

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
