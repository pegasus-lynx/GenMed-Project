from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='homepage'),
    path('login/',views.logIn, name='logIn'),
    path('register/',views.register, name='register'),
]