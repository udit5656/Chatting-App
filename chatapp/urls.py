from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('chat/<int:sender_id>/<int:reciever_id>/', views.confirmpage, name='confirmpage'),
    path('chat/<int:sender_id>/<int:reciever_id>/messages', views.chatpage, name='chatpage'),
    path('chat/<int:sender_id>/<int:reciever_id>/delete-message/<int:message_id>/', views.delete_chat_message,
         name="delete_chat_message"),
    path('chat/group-chat/', views.group_chat, name='group_chat'),
    path('chat/group-chat/<str:group_name>/<int:sender_id>/messages', views.group_chat_messages,
         name='group_chat_messages'),
    path('chat/chat-redirecter/<int:sender_id>/<int:chat_id>/', views.user_chat_redirecter,
         name='user_chat_redirecter'),
    path('chat/group-chat/create/', views.create_group, name='create_group'),
    path('chat/group-chat/delete/<str:group_name>', views.delete_group, name='delete_group')
]
