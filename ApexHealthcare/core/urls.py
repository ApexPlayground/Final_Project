from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

path('', views.home, name='home'),
path('register', views.registerView, name='reg'),

















]