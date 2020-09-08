from django import template
from django.apps import apps
from django.contrib.auth.models import User

register = template.Library()
Message = apps.get_model('chatapp', 'Message')


@register.simple_tag()
def other_member(user_chat, user):
    if user_chat.member_one == user:
        return user_chat.member_two.username
    else:
        return user_chat.member_one.username


@register.simple_tag()
def unread_messages_count(user_chat, user):
    reciever_username = other_member(user_chat, user)
    reciever_user = User.objects.get(username=reciever_username)
    unread_messages = Message.objects.filter(sender=reciever_user, reciever=user, unread=True).count()
    return unread_messages
