from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('', views.home, name='home'),
    #path('chat/<int:sender_id>/<int:reciever_id>/', views.confirmpage, name='confirmpage'),
    path('chat/<int:sender_id>/<int:reciever_id>/messages', views.chatpage, name='chatpage'),
]
