from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('chatapp:home'))
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('chatapp:home'))
            messages.add_message(request, messages.INFO, 'Wrong Credentials')
            return HttpResponseRedirect(reverse('accounts:login'))
        return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('chatapp:home'))
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('chatapp:home'))
            return render(request, 'accounts/signup.html', {'form': form})
        form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
