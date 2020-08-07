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
