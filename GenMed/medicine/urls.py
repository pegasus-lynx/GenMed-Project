from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('info',views.query_medinfo, name='info'),
    path('avail',views.query_medavail, name='avail'),
]