from django import forms


class UserSearchForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=50)


class MessageForm(forms.Form):
    message_text = forms.CharField(label="Enter message", max_length=50)
