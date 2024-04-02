from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

path('', views.home, name='home'),
path('register/', views.registerView, name='reg'),
path('reg_user/', views.registerUser, name='reg_user'),
path('login/', views.loginView, name='login'),


















]