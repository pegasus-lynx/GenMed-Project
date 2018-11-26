from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.logIn, name='logIn'),
    path('logout/',views.logOut, name='logOut'),
    path('register/',views.register, name='register'),
    path('createshop/',views.createshop, name='create_shop'),
    path('sqlerror/', views.sqlerror, name = 'sqlerror')
]