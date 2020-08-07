from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_user/', views.check_user, name='searchuser')
]
