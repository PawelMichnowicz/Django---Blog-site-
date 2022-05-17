from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from django.contrib.auth.models import User 

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from content.models import Tweet, Comment, Action
from account.models import Profile


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ImageSerializer(many=False, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = User
        fields = ['id','url', 'username', 'profile']


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type":'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = { 'password': {'write_only':True} }

    def create(self):
        user = User(email = self.validated_data['email'],
                    username = self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Hasła różnią się od siebie'})
        user.set_password(password)
        user.save()
        return user

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    profile = ImageSerializer(many=False, read_only=True)
    posts = serializers.HyperlinkedIdentityField(view_name="api:user-post", lookup_field='id')
    num_posts = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    num_hits = serializers.SerializerMethodField()

    def get_num_comments(self, obj):
        num_comments = obj.comments.all().count()
        return num_comments
    
    def get_num_likes(self, obj):
        num_likes = obj.likes.all().count()
        return num_likes

    def get_num_posts(self, obj):
        num_posts = obj.posts.all().count()
        return num_posts

    def get_num_hits(self, obj):
        num_hits = obj.profile.num_of_hits
        return num_hits

    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'num_posts', 'posts', 'num_comments', 'num_likes', 'num_hits']
        


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text']





class TweetSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='api:tweet-router-detail')
    author = serializers.HyperlinkedRelatedField( read_only=True, view_name='api:user-detail')
    num_comments = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()

    def get_num_comments(self, obj):
        num_comments = obj.comments.all().count()
        return num_comments
    
    def get_num_likes(self, obj):
        num_likes = obj.users_like.all().count()
        return num_likes

    class Meta:
        model = Tweet
        fields = ['id', 'url', 'title', 'text', 'author', 'num_comments', 'num_likes',]



class TweetDetailSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.HyperlinkedRelatedField( read_only=True, view_name='api:user-detail')
    like_url = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comment_url = serializers.SerializerMethodField()


    class Meta:
        model = Tweet
        fields = ['id', 'title', 'text', 'author','num_likes', 'like_url', 'comment_url', 'comments', ]

    ###### nie wiem jak ustawić odpowiedni formularz żeby wyświatlała się tylko kolumna 'text', aktualnie wyświetla sie 'title' i 'text'  - próba 1
    ###### nie wyświetla mi się w ogóle html form do wstawiania komentarza - próba 2
    def get_comment_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse(viewname='api:tweet-router-comment', kwargs={'pk':obj.pk}, request=request) #próba 1
        return reverse(viewname='api:comment', kwargs={'pk':obj.pk}, request=request) # próba 2

    
    def get_num_likes(self, obj):
        num_likes = obj.users_like.all().count()
        return num_likes

    def get_like_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse(viewname='api:tweet-router-like', kwargs={'pk':obj.pk}, request=request)


class ActionSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField( read_only=True, view_name='api:user-detail')
    post = serializers.HyperlinkedRelatedField( read_only=True, view_name='api:tweet-router-detail', source='content_object')

    class Meta:
        model = Action
        fields = ['id', 'user', 'verb', 'post']


#      class TweetSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True)
#     author = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field = 'pk', format='html')
#     url = serializers.HyperlinkedIdentityField(view_name="api:tweet-detail")

#     class Meta:
#         model = Tweet
#         fields = ['id','url', 'author', 'title', 'text', 'comments', 'users_like']




