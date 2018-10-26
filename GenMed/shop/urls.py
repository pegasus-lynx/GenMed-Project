from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('update-stock',views.update-stock, name='update-stock')
    path('shop-profile/',views.shop-profile, name='shop-profile'),
    path('cur-stock/',views.cur-stock, name='cur-stock'),
    path('update-profile/',views.update-profile, name='update-profile'),
]