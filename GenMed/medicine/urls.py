from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='med-home'),
    path('med-info',views.query_medinfo, name='med-info'),
    path('med-avail',views.query_medavail, name='med-avail')
]