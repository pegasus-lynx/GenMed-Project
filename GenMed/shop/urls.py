from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('update/stock',views.update_stock, name='update_stock'),
    path('profile/',views.profile, name='profile'),
    path('curstock/',views.curstock, name='curstock'),
    path('update/info/',views.update_info, name='update_info'),
    path('update/cord', views.update_cord, name='update_cord'),
    path('update/license', views.update_license, name='update_license'),
    path('shop_header/',views.shopheader, name='shopheader'),
]