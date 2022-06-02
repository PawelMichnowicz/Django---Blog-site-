from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from . import forms

app_name = 'account'

urlpatterns = [
    path('detail/', views.UserSettings.as_view(), name='detail'), # for changing avatar/password of request user
    path('user-detail/<str:username>/', views.UserDetail.as_view(), name='user_detail'), # info about choosen user (number of posts/comments)
    path('register/', views.Register.as_view(), name='register'),
    path('login/', forms.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')), # include password change and passoword reset views
    

]
