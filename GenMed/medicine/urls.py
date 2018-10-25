from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.home, name='med-home'),
    path('med-info',views.query_medinfo, name='med-info'),
    path('med-avail',views.query_medavail, name='med-avail')
]