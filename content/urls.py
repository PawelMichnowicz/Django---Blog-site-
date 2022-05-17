from re import A
from django.urls import path

from . import views

app_name = 'content'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # main page with content ( activity log and top user/posts)
    path('dash-posts-ajax/', views.dash_posts_ajax, name='dash_posts_ajax'), # ajax source of content for statistic with top posts
    path('dash-users-ajax/', views.dash_users_ajax, name='dash_users_ajax'), # same with top users
    path('list/<str:username>/', views.list, name='user_list'), # list of posts for particular user
    path('list/', views.list, name='list'), # list of all posts
    path('create/', views.create, name='create'), # url for create post
    path('edit/<slug:slug>/', views.post_edit, name='post_edit'), # editing particular post 
    path('detail/<slug:slug>/', views.post_detail, name='detail'), # url path for detail view of post (include comments)
    path('post-like/', views.post_like, name='post_like'), # ajax url for like action by ajax

]