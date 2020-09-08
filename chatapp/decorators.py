from django.core.exceptions import PermissionDenied
from .models import Message


def user_can_see_chat(function):
    def wrap(request, *args, **kwargs):
        if request.user.id != kwargs['sender_id']:
            raise PermissionDenied
        else:
            return function(request, *args, **kwargs)

    return wrap


def user_can_delete_message(function):
    def wrap(request, *args, **kwargs):
        message = Message.objects.get(pk=kwargs['message_id'])
        if request.user.id == message.sender.id:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
