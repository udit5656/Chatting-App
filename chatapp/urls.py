from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('chat/<int:sender_id>/<int:reciever_id>/messages', views.chatpage, name='chatpage'),
    path('chat/<int:sender_id>/<int:reciever_id>/delete-message/<int:message_id>/', views.delete_chat_message,
         name="delete_chat_message"),
    path('chat/chat-redirecter/<int:sender_id>/<int:chat_id>/', views.user_chat_redirecter,
         name='user_chat_redirecter'),
]
