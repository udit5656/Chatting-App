from django.core.exceptions import PermissionDenied
from .models import Group, GroupMessage


def user_is_group_member(function):
    def wrap(request, *args, **kwargs):
        group = Group.objects.get(group_name=kwargs['group_name'])
        if group.members.all().filter(username=request.user.username).count() < 1:
            raise PermissionDenied
        else:
            return function(request, *args, **kwargs)

    return wrap


def user_is_group_admin(function):
    def wrap(request, *args, **kwargs):
        group = Group.objects.get(group_name=kwargs['group_name'])
        if request.user.username == group.admin:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_can_delete_group_message(function):
    def wrap(request, *args, **kwargs):
        message = GroupMessage.objects.get(pk=kwargs['message_id'])
        if request.user.id == message.sender.id:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_can_send_group_message(function):
    def wrap(request, *args, **kwargs):
        if request.user.id == kwargs['sender_id']:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
