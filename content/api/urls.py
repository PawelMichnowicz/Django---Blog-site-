from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet, basename='post-router')
router.register('actions', views.ActionViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('user-posts/<int:id>/',
         views.PostUserViewSet.as_view({'get': 'list'}), name='user-post'),
    path('user-registration', views.RegisterUser.as_view(), name='register'),
    path('comment-post/<int:pk>/', views.CommentCreate.as_view(),
         name='comment')  # nie wyświetla form html

]
