from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,  AllowAny, BasePermission
from rest_framework.decorators import action


from django.contrib.auth.models import User 
from ..models import Tweet, Action, Comment
from .serializers import TweetSerializer, UserSerializer, UserDetailSerializer, TweetDetailSerializer, ActionSerializer, CommentSerializer
from ..utils import make_action
from .permissions import TweetPermission

from rest_framework.mixins import ListModelMixin


class UserViewSet(viewsets.ReadOnlyModelViewSet): 

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer


class TweetViewSet(viewsets.ModelViewSet): 

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [TweetPermission, IsAuthenticated] 
    

    def perform_create(self, serializer):
        model = serializer.save()
        make_action(user=self.request.user , verb='utworzył', content_object=model)

    def perform_update(self, serializer):
        model = serializer.save()
        make_action(user=self.request.user , verb='edytował', content_object=model)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TweetDetailSerializer
        return TweetSerializer

                #     Próba przypisania możliwości formy do tworzenia komentarza, brak 
    # def post(self, request, *args, **kwargs): 
    ##### if detail_view :
    #     text = request.data['text']
    #     author = request.user
    #     post = self.get_object()
    #     new_comment = Comment.objects.create(post=post, author=author, text=text)
    #     new_comment.save()
    #     make_action(user=author, verb='skomentował', content_object=post)
    #     return Response({'Comment':"Yes"})



    @action(detail=True, methods=['post'])
    def comment(self, request, *args, **kwargs): 

        post = self.get_object()
        author = request.user
        text = request.data['text']
        new_comment = Comment.objects.create(post=post, author=author, text=text)
        new_comment.save()
        make_action(user=author, verb='skomentował', content_object=post)
        return Response({'Commented':True})


    @action(detail=True, methods=['post', 'get'], url_path="like", url_name="like")
    def like(self, request,  *args, **kwargs):
        post = self.get_object()
        if not request.user in post.users_like.all():
            post.users_like.add(request.user)
            make_action(request.user, 'polubił', post)
            return Response({"liked":True})
        else:
            return Response({"liked":False})


class TweetUserViewSet(TweetViewSet):

    def get_queryset(self):
        username = self.kwargs['id']
        return Tweet.objects.filter(author=username)


class ActionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



# class TweetListView(generics.ListAPIView):
#     queryset = Tweet.objects.all()
#     serializer_class = TweetSerializer

# class TweetDetailView(generics.RetrieveAPIView):
#     queryset = Tweet.objects.all()
#     serializer_class = TweetSerializer

# class TweetLikeView(APIView):
#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, pk, format=None):
#         post = get_object_or_404(Tweet, pk=pk)
#         post.users_like.add(request.user)
#         make_action(request.user, 'polubił', post)
#         return Response({"liked":True})


