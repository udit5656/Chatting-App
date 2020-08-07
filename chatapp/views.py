from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserSearchForm


# Create your views here.

def index(request):
    form = UserSearchForm()
    context = {'form': form}
    return render(request, 'chatapp/index.html', context)


def check_user(request):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                return HttpResponse("working")
            except User.DoesNotExist:
                form.add_error('username',ValidationError("User doesnot exist"))
        return render(request, 'chatapp/index.html', {'form': form})
    else:
        form = UserSearchForm()
    return render(request, 'chatapp/index.html', {'form': form})
