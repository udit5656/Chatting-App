from django.contrib import admin
from .models import Message, Group, GroupMessage

# Register your models here.
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(GroupMessage)
