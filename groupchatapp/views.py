from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import GroupCreationForm, GroupSearchForm, MessageForm
from .models import Group, GroupMessage
from .decorators import user_is_group_member, user_is_group_admin, user_can_delete_group_message, \
    user_can_send_group_message


@login_required
def group_chat(request):
    if request.method == 'POST':
        form = GroupSearchForm(request.POST)
        if form.is_valid():
            try:
                group = Group.objects.get(group_name=form.cleaned_data['groupname'])
                group_code = form.cleaned_data['groupcode']
                if group_code == group.group_code and group.check_for_vacancy():
                    context = {'group_name': group.group_name, 'sender_id': request.user.id}
                    group.members.add(request.user)
                    return HttpResponseRedirect(reverse('groupchatapp:group_chat_messages', kwargs=context))
                if not group.check_for_vacancy():
                    form.add_error('groupname', ValidationError('Group is full'))
                else:
                    form.add_error('groupname', ValidationError('Wrong Credentials'))
            except Group.DoesNotExist:
                form.add_error('groupname', ValidationError("Group doesn't exist"))
        return render(request, 'groupchatapp/group_page.html', {'form': form})
    form = GroupSearchForm()
    return render(request, 'groupchatapp/group_page.html', {'form': form})


@login_required
@user_is_group_member
@user_can_send_group_message
def group_chat_messages(request, group_name, sender_id):
    group = Group.objects.get(group_name=group_name)
    sender = User.objects.get(pk=sender_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_txt = form.cleaned_data['message_text']
            message = GroupMessage.create(message_text=message_txt, sender=sender, group=group)
            message.save()
    form = MessageForm()
    group_messages = GroupMessage.objects.all().filter(group=group).order_by('send_time')
    context = {'group_name': group_name, 'sender_id': sender_id, 'messages': group_messages, 'form': form,
               'members': group.members.all(), 'admin': group.admin, 'group_code': group.group_code}
    return render(request, 'groupchatapp/group_chat.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['groupname']
            group_code = form.cleaned_data['groupcode']
            try:
                group = Group.objects.all().get(group_name=group_name)
                form.add_error('groupname', ValidationError('This group name is not available'))
                return render(request, 'chatapp/create_group_page.html', {'form': form})
            except Group.DoesNotExist:
                group = Group.create(group_name=group_name, group_code=group_code, admin=request.user.username)
                group.save()
                group.members.add(request.user)
                context = {'group_name': group_name, 'sender_id': request.user.id}
                return HttpResponseRedirect(reverse('groupchatapp:group_chat_messages', kwargs=context))
        return render(request, 'chatapp/create_group_page.html', {'form': form})
    form = GroupCreationForm()
    return render(request, 'groupchatapp/create_group_page.html', {'form': form})


@login_required
@user_is_group_admin
def delete_group(request, group_name):
    group = Group.objects.get(group_name=group_name)
    group.delete()
    return HttpResponseRedirect(reverse('chatapp:home'))


@login_required
@user_is_group_member
@user_can_delete_group_message
def delete_group_message(request, group_name, message_id):
    message = GroupMessage.objects.get(pk=message_id)
    message.delete()
    context = {'group_name': group_name, 'sender_id': request.user.id}
    return HttpResponseRedirect(reverse('groupchatapp:group_chat_messages', kwargs=context))
