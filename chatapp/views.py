from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Message

from .forms import UserSearchForm, MessageForm


# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                context = {'sender_id': request.user.pk, 'reciever_id': user.pk}
                return HttpResponseRedirect(reverse('chatapp:chatpage', kwargs=context))
            except User.DoesNotExist:
                form.add_error('username', ValidationError("User Doesn't Exist"))
        return render(request, 'chatapp/home.html', {'form': form})
    else:
        form = UserSearchForm()
    return render(request, 'chatapp/home.html', {'form': form})


def chatpage(request, sender_id, reciever_id):
    if request.method == 'GET':
        form = MessageForm()
        sender = User.objects.get(pk=sender_id)
        reciever = User.objects.get(pk=reciever_id)
        messages = Message.objects.filter((Q(sender=sender) | Q(sender=reciever)),
                                          (Q(reciever=reciever) | Q(reciever=sender))).order_by("send_time")
        context = {'sender': sender, 'reciever': reciever, 'messages': messages, 'form': form}
        return render(request, 'chatapp/chatpage.html', context)
    else:
        form = MessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            sender = User.objects.get(pk=sender_id)
            reciever = User.objects.get(pk=reciever_id)
            new_message = Message.create(msg_text=message_text, sender=sender, reciever=reciever)
            new_message.save()
            messages = Message.objects.filter((Q(sender=sender) | Q(sender=reciever)),
                                              (Q(reciever=reciever) | Q(reciever=sender))).order_by("send_time")
            form = MessageForm()
            context = {'sender': sender, 'reciever': reciever, 'messages': messages, 'form': form}
            return render(request, 'chatapp/chatpage.html', context)
