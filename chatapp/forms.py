from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserSearchForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=50)


class MessageForm(forms.Form):
    message_text = forms.CharField(label="Enter message", max_length=50)


class GroupSearchForm(forms.Form):
    groupname = forms.CharField(label="Group Name", max_length=50)
