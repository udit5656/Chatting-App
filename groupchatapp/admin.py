from django.contrib import admin
from .models import GroupMessage, Group

# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMessage)
