from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.TweetViewSet, basename='tweet-router')
router.register('actions', views.ActionViewSet)


app_name = 'api'

urlpatterns = [

    #path('posts/<pk>/like/', views.TweetLikeView.as_view(), name='post_like'),
    # path('posts/', views.TweetListView.as_view(), name='posts_list'),
    # path('posts/<pk>/', views.TweetDetailView.as_view(), name='post_detail'),
    # path('users/', user_list , name='user-list'),
    # path('users/<int:pk>/', user_detail, name='user-detail'),
    path('', include(router.urls)),
    path('user-tweets/<int:id>/', views.TweetUserViewSet.as_view({'get': 'list'}), name='user-post'),
    path('user-registration', views.RegisterUser.as_view(), name='register'),
    path('comment-tweet/<int:pk>/', views.CommentCreate.as_view(), name='comment' ) # nie wyświetla form html

]