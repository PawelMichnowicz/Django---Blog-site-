from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from content.models import Post, Comment, Action
from account.models import Profile

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


class UserSerializer(serializers.ModelSerializer):
    profile = ImageSerializer(many=False, read_only=True)
    url_profile = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = get_user_model()
        fields = ['id', 'url_profile', 'username', 'profile']


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={"input_type": 'password'}, write_only=True)
    password = serializers.CharField(
        style={"input_type": 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, data):
        if not data.get('password') or not data.get('password2'):
            raise serializers.ValidationError("Wprowadź oba hasła")
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Hasła nie są identyczne")
        return data

    def create(self, validated_data): # 
        user = get_user_model().objects.create_user(email=self.validated_data['email'],
                    username=self.validated_data['username'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ImageSerializer(many=False, read_only=True)
    posts = serializers.HyperlinkedIdentityField(
        view_name="api:user-post", lookup_field='id')
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
        model = get_user_model()
        fields = ['id', 'username', 'profile', 'num_posts',
                  'posts', 'num_comments', 'num_likes', 'num_hits']



class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True) 

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text']


class PostSerializer(serializers.ModelSerializer):

    url_post = serializers.HyperlinkedIdentityField(
        view_name='api:post-router-detail')
    author = UserSerializer(many=False, read_only=True) 
    num_comments = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()

    def get_num_comments(self, obj):
        num_comments = obj.comments.all().count()
        return num_comments

    def get_num_likes(self, obj):
        num_likes = obj.users_like.all().count()
        return num_likes

    class Meta:
        model = Post
        fields = ['id', 'url_post', 'title', 'text',
                  'author', 'num_comments', 'num_likes', ]


class PostDetailSerializer(serializers.ModelSerializer):

    author = UserSerializer(many=False, read_only=True) 
    like_url = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comment_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'author', 'num_likes',
                  'like_url', 'comment_url', 'comments', ]

    def get_num_likes(self, obj):
        num_likes = obj.users_like.all().count()
        return num_likes

    def get_like_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse(viewname='api:post-router-like', kwargs={'pk': obj.pk}, request=request)


class ActionSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api:user-detail')
    post = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api:post-router-detail', source='content_object')

    class Meta:
        model = Action
        fields = ['id', 'user', 'verb', '']

