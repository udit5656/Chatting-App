from django.urls import path
from . import views

app_name = 'groupchatapp'
urlpatterns = [
    path('', views.group_chat, name='group_chat'),
    path('<str:group_name>/<int:sender_id>/messages/', views.group_chat_messages, name='group_chat_messages'),
    path('create/', views.create_group, name='create_group'),
    path('delete/<str:group_name>/', views.delete_group, name='delete_group'),
    path('delete_group_message/<str:group_name>/<int:message_id>/', views.delete_group_message, name="delete_group_message"),
]
