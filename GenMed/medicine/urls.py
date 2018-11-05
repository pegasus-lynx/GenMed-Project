from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='med-home'),
    path('info',views.query_medinfo, name='med-info'),
 #   path('avail',views.query_medavail, name='med-avail'),
]