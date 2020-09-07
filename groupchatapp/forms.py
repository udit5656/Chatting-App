from django import forms


class MessageForm(forms.Form):
    message_text = forms.CharField(label="Enter message", max_length=500)


class GroupSearchForm(forms.Form):
    groupname = forms.CharField(label="Group Name", max_length=50)
    groupcode = forms.CharField(label="Group Code", max_length=50)


class GroupCreationForm(forms.Form):
    groupname = forms.CharField(label="Group Name", max_length=50)
    groupcode = forms.CharField(label="Group Code", max_length=50)
