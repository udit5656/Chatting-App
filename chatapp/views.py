from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import Message, Chat
from .decorators import user_can_see_chat, user_can_delete_message
from .forms import UserSearchForm, MessageForm


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
        user_groups = request.user.group_members.all()
        return render(request, 'chatapp/home.html', {'form': form, 'user_groups': user_groups})

    def get(self, request):
        form = UserSearchForm()
        user_groups = request.user.group_members.all()
        user_chats =Chat.objects.filter(Q(member_one=request.user) | Q(member_two=request.user)).order_by(
            '-last_message_time')
        return render(request, 'chatapp/home.html',
                      {'form': form, 'user_groups': user_groups, 'user_chats': user_chats})


@login_required
@user_can_see_chat
def user_chat_redirecter(request, sender_id, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    if chat.member_one.pk == sender_id:
        context = {'sender_id': sender_id, 'reciever_id': chat.member_two.pk}
    else:
        context = {'sender_id': sender_id, 'reciever_id': chat.member_one.pk}
    return HttpResponseRedirect(reverse('chatapp:chatpage', kwargs=context))


@login_required
@user_can_see_chat
def chatpage(request, sender_id, reciever_id):
    sender = User.objects.get(pk=sender_id)
    reciever = User.objects.get(pk=reciever_id)
    messages = Message.objects.filter((Q(sender=sender) | Q(sender=reciever)),
                                      (Q(reciever=reciever) | Q(reciever=sender))).order_by("send_time")
    unread_messages = Message.objects.filter(sender=reciever, reciever=sender, unread=True)
    for unread_message in unread_messages:
        unread_message.unread = False
        unread_message.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            new_message = Message.create(msg_text=message_text, sender=sender, reciever=reciever)
            new_message.save()
            if not Chat.objects.filter(Q(member_one=sender) | Q(member_one=reciever),
                                       (Q(member_two=sender) | Q(member_two=reciever))).exists():
                chat = Chat.create(latest_message=new_message, member_one=sender, member_two=reciever)
                chat.save()
            else:
                chat = Chat.objects.get(Q(member_one=sender) | Q(member_one=reciever),
                                        (Q(member_two=sender) | Q(member_two=reciever)))
                chat.update_latest_message(new_message)

    form = MessageForm()
    context = {'sender': sender, 'reciever': reciever, 'messages': messages, 'form': form}
    return render(request, 'chatapp/chatpage.html', context)


@login_required
@user_can_delete_message
def delete_chat_message(request, sender_id, reciever_id, message_id):
    message = Message.objects.get(pk=message_id)
    if Chat.objects.filter(latest_message=message).exists():
        chat = Chat.objects.get(latest_message=message)
        chat.delete_latest_message()
    message.delete()
    context = {'sender_id': sender_id, 'reciever_id': reciever_id}
    return HttpResponseRedirect(reverse('chatapp:chatpage', kwargs=context))
