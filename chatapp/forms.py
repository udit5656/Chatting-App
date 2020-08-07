from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserSearchForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=50)

