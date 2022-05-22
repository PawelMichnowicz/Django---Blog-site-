from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,  AllowAny
from rest_framework.decorators import action
from knox.auth import TokenAuthentication

from ..models import Post, Action, Comment
from .serializers import PostSerializer, UserSerializer, UserDetailSerializer, UserRegistrationSerializer, PostDetailSerializer, ActionSerializer, CommentSerializer
from ..utils import make_action
from .permissions import PostPermission


class RegisterUser(generics.GenericAPIView):
    # registration view
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data['Response'] = 'Założono konto'
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        # chose proper serializer for retrieve (detail view) or list of users
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = [PostPermission, IsAuthenticated]

    def perform_create(self, serializer):
        # add activity log after create post
        model = serializer.save()
        make_action(user=self.request.user,
                    verb='utworzył', content_object=model)

    def perform_update(self, serializer):
        # add activity log after edit post
        model = serializer.save()
        make_action(user=self.request.user,
                    verb='edytował', content_object=model)

    def get_serializer_class(self):
        # choose proper serializer for retrive or list
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'], url_name='comment')
    # action for giving comment
    # nie wiem jak ustawić odpowiedni formularz żeby wyświatlała się tylko kolumna 'text', aktualnie wyświetla sie 'title' i 'text'
    # próba 2
    def comment(self, request, *args, **kwargs):
        post = self.get_object()
        author = request.user
        text = request.data['text']
        new_comment = Comment.objects.create(
            post=post, author=author, text=text)
        new_comment.save()
        make_action(user=author, verb='skomentował', content_object=post)
        return Response({'Commented': True})

    @action(detail=True, methods=['post', 'get'], url_name="like")
    # action for giving likes
    def like(self, request,  *args, **kwargs):
        post = self.get_object()
        if not request.user in post.users_like.all():
            post.users_like.add(request.user)
            make_action(request.user, 'polubił', post)
            return Response({"liked": True})
        else:
            return Response({"liked": False})


class PostUserViewSet(PostViewSet):
    # view inherit after PostViewSet, shows posts from particular user
    def get_queryset(self):
        username = self.kwargs['id']
        return Post.objects.filter(author=username)


class ActionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class CommentCreate(generics.CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = CommentSerializer

    # próba 1
    def post(self, request, *args, **kwargs):
        serializer = Comment(data=request.data)
        if serializer.is_valid():
            post = Post.objects.get(id=1)
            author = request.user
            text = serializer.text
            new_comment = Comment(post=post, author=author, text=text)
            data = {'powstał': new_comment.post}
        else:
            data = {'coś:nie tak'}
        return Response(data)

    # @action(detail=True, methods=['post'], url_name='comment')
    # ###### nie wyświetla się żaden html form
    # def comment(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     author = request.user
    #     text = request.data['text']
    #     new_comment = Comment.objects.create(post=post, author=author, text=text)
    #     new_comment.save()
    #     make_action(user=author, verb='skomentował', content_object=post)
    #     return Response({'Commented':True})


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
