from rest_framework import serializers
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User 
from django.urls import reverse, reverse_lazy


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

    url = serializers.HyperlinkedIdentityField(view_name="api:tweet-detail")
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
    comments = CommentSerializer(many=True, read_only=True)
    num_likes = serializers.SerializerMethodField()

    #raise Exception(reverse(api:user-detail'))
    #like = serializers.Hyperlink(url=reverse('api:Posts-post-like'))
    # raise Exception(reverse_lazy('api:like'))

    def get_num_likes(self, obj):
        num_likes = obj.users_like.all().count()
        return num_likes

    class Meta:
        model = Tweet
        fields = ['id', 'title', 'text', 'author', 'comments', 'num_likes']


class ActionSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField( read_only=True, view_name='api:user-detail')
    post = serializers.HyperlinkedRelatedField( read_only=True, view_name='api:tweet-detail', source='content_object')

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




