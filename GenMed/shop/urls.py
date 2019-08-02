from django.urls import path
from . import views
from .feeds import ShopCommentFeed

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('updatestock/',views.update_stock, name='update_stock'),
    path('addmed/',views.add_med, name='add_med'),
    path('updatemed/',views.update_med, name='update_med'),
    path('search/', views.search, name='search'),
    path('profile/<int:shop_id>',views.profile, name='profile'),
    path('curstock/',views.cur_stock, name='cur_stock'),
    path('updateinfo/',views.update_info, name='update_info'),
    path('updatecord/', views.update_cord, name='update_cord'),
    path('updatelicense/', views.update_license, name='update_license'),
    path('license/', views.license, name='license'),
    path('home/', views.home, name='home'),
    path('shopcomments/', ShopCommentFeed(), name='shopcomments'),
    path('feeds/<int:comment_no>/', views.feeds, name='feeds'),
    path('comment/', views.comment, name='comment'),
    path('map/', views.map, name='map_test')
]