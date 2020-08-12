from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import Message, Group, GroupMessage

from .forms import UserSearchForm, MessageForm, GroupSearchForm, GroupCreationForm


# Create your views here.
@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def post(self, request):
        form = UserSearchForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                context = {'sender_id': request.user.pk, 'reciever_id': user.pk}
                return HttpResponseRedirect(reverse('chatapp:chatpage', kwargs=context))
            except User.DoesNotExist:
                form.add_error('username', ValidationError("User Doesn't Exist"))
        return render(request, 'chatapp/home.html', {'form': form})

    def get(self, request):
        form = UserSearchForm()
        return render(request, 'chatapp/home.html', {'form': form})


def chatpage(request, sender_id, reciever_id):
    sender = User.objects.get(pk=sender_id)
    reciever = User.objects.get(pk=reciever_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            new_message = Message.create(msg_text=message_text, sender=sender, reciever=reciever)
            new_message.save()

    messages = Message.objects.filter((Q(sender=sender) | Q(sender=reciever)),
                                      (Q(reciever=reciever) | Q(reciever=sender))).order_by("send_time")
    form = MessageForm()
    context = {'sender': sender, 'reciever': reciever, 'messages': messages, 'form': form}
    return render(request, 'chatapp/chatpage.html', context)


@login_required
def group_chat(request):
    if request.method == 'POST':
        form = GroupSearchForm(request.POST)
        if form.is_valid():
            try:
                group = Group.objects.get(group_name=form.cleaned_data['groupname'])
                group_code = form.cleaned_data['groupcode']
                if group_code == group.group_code:
                    context = {'group_name': group.group_name, 'sender_id': request.user.id}
                    return HttpResponseRedirect(reverse('chatapp:group_chat_messages', kwargs=context))
                form.add_error('groupname',ValidationError('Wrong Credentials'))
            except Group.DoesNotExist:
                form.add_error('groupname', ValidationError("Group doesn't exist"))
        return render(request, 'chatapp/group_page.html', {'form': form})
    form = GroupSearchForm()
    return render(request, 'chatapp/group_page.html', {'form': form})


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
    context = {'group_name': group_name, 'sender_id': sender_id, 'messages': group_messages, 'form': form}
    return render(request, 'chatapp/group_chat.html', context)


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
                group = Group.create(group_name=group_name, group_code=group_code)
                group.save()
                group.members.add(request.user)
                context = {'group_name': group_name, 'sender_id': request.user.id}
                return HttpResponseRedirect(reverse('chatapp:group_chat_messages', kwargs=context))
        return render(request, 'chatapp/create_group_page.html', {'form': form})
    form = GroupCreationForm()
    return render(request, 'chatapp/create_group_page.html', {'form': form})
