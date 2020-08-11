from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('chat/<int:sender_id>/<int:reciever_id>/', views.confirmpage, name='confirmpage'),
    path('chat/<int:sender_id>/<int:reciever_id>/messages', views.chatpage, name='chatpage'),
    path('chat/grouppage/', views.group_page, name='group_page'),
    path('chat/grouppage/<str:group_name>/<int:sender_id>/', views.group_chat, name='group_chat')
]
