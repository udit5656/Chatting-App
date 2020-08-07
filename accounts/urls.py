from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('index/', views.login_user, name='index'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup')
]
