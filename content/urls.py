from django.urls import path

from . import views

app_name = 'content'

urlpatterns = [
    #path('', views.dashboard, name='dashboard'), 
    #path('dash-posts-ajax/', views.dash_posts_ajax, name='dash_posts_ajax')
     #path('dash-users-ajax/', views.dash_users_ajax, name='dash_users_ajax'), 
    path('', views.DashboardView.as_view(), name='dashboard'), # main page with content ( activity log and top user/posts)
    path('dash-posts-ajax/', views.DashboardPosts.as_view(), name='dash_posts_ajax'), # ajax source of content for statistic with top posts
    path('dash-users-ajax/', views.DashboardUsers.as_view(), name='dash_users_ajax'), # same with top users
    
    path('list/<str:username>/', views.PostUserList.as_view(), name='user_list'), # list of posts for particular user
    #path('list/<str:username>/', views.list, name='user_list'),
    path('list/', views.PostList.as_view(), name='list'), # list of all posts
    #path('list/', views.list, name='list'), # list of all posts
    path('create/', views.CreatePost.as_view(), name='create'),
    #path('create/', views.create, name='create'), # url for create post 
    path('edit/<slug:slug>/', views.UpdatePost.as_view(), name='post_edit'), # editing particular post 
    #path('edit/<slug:slug>/', views.post_edit, name='post_edit'),
    path('delete/<slug:slug>', views.DeletePost.as_view(), name='post-delete'),
    path('detail/<slug:slug>/', views.DetailPost.as_view(), name='detail'),
    #path('detail/<slug:slug>/', views.post_detail, name='detail'), # url path for detail view of post (include comments)
    path('post-like/', views.post_like, name='post_like'), # ajax url for like action by ajax

]