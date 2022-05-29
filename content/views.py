from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F
from django.views.generic import View, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy


from .models import Post, Action
from .forms import NewPostForm, NewCommentForm, ChoiceOrderForm, EditPostForm, ShowPost, ShowUsers
from .utils import make_action



class DashboardView(TemplateView):
    template_name = 'content/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'main'
        context['actions'] = Action.objects.all()[:18]
        return context


class DashboardUsers(FormView):
    template_name = 'content/dash_users_ajax.html'
    form = ShowUsers()
    users = None

    def get(self, request, *args, **kwargs):
        choice = self.request.GET.get('choice')
        form = ShowUsers(self.request.GET or None)
        if form.is_valid():
            choice = form.cleaned_data['choice']  # choice from ShowUsers form
            self.users = get_user_model().objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count('likes', distinct=True), hits=F('profile__num_of_hits'))  # addding stats of number of comments/likes/hits to users
            self.users = self.users.order_by(choice)[:5]
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['section'] = 'main'
        #context['form'] = self.form
        context['users'] = self.users
        return context


class DashboardPosts(FormView):
    template_name = 'content/dash_posts_ajax.html'
    form = ShowPost()
    posts = None

    def get(self, request, *args, **kwargs):
        choice = self.request.GET.get('choice')
        form = ShowPost(self.request.GET or None)
        if form.is_valid():
            choice = form.cleaned_data['choice']  # choice from ShowPost form
            self.posts = Post.objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count(
                'users_like', distinct=True))  # addding stats of number of comments/likes/hits to users
            self.posts = self.posts.order_by(choice)[:5]
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['section'] = 'main'
        #context['form'] = self.form
        context['posts'] = self.posts
        return context

'''
def dashboard(request):
    # view with top 18 activity logs
    actions = Action.objects.all()[:18]
    return render(request, 'content/dashboard.html', {'section': 'main', 'actions': actions})

def dash_users_ajax(request):
    # ajax view source for top users
    users = None
    form = ShowUsers()  # form for choice param
    choice = None
    if 'choice' in request.GET:
        form = ShowUsers(request.GET)
        if form.is_valid():
            choice = form.cleaned_data['choice']  # choice from ShowUsers form
            users = get_user_model().objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count(
                'likes', distinct=True), hits=F('profile__num_of_hits'))  # addding stats of number of comments/likes/hits to users
            users = users.order_by(choice)[:5]  # ordering

    return render(request, 'content/dash_users_ajax.html', {'section': 'main', 'users': users, 'form': form, "choice": choice})

def dash_posts_ajax(request):
    # ajax view source for top posts
    posts = None
    form = ShowPost()
    choice = None
    choice_label = None
    if 'choice' in request.GET:
        form = ShowPost(request.GET)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            posts = Post.objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count(
                'users_like', distinct=True))  # addding stats of number of comments/likes/hits to users
            posts = posts.order_by(choice)[:5]

    return render(request, 'content/dash_posts_ajax.html', {'section': 'main', 'posts': posts, 'form': form, "choice": choice, })
'''

class PostList(ListView):

    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.annotate(num_comments=Count('comments', distinct=True), 
                                    num_likes=Count('users_like', distinct=True)
                                    )

    def choice(self):
        choice = self.request.GET.get('choice')
        if choice == None:
            choice = '-date_create'
        return choice

    def get_template_names(self):
        template_name = 'content/list.html'
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            template_name = 'content/list_ajax.html'
        return template_name
    
    def paginate_queryset(self, queryset, page_size) :
        queryset = self.queryset.order_by(self.choice()) 
        return super().paginate_queryset(queryset, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice'] = self.choice()
        context['form'] = ChoiceOrderForm(self.request.GET)
        context['section'] = 'blog'
        context['user'] = None
        return context


class PostUserList(PostList):
    
    def username(self):
        return self.kwargs['username']

    def get_queryset(self):
        user = get_user_model().objects.get(username=self.username())
        posts = Post.objects.filter(author=user)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_user_model().objects.get(username=self.username()) 
        context['form'] = None
        return context

@require_POST
def post_like(request):
    # ajax view for adding like
    id = request.POST.get('id')
    action = request.POST.get('action')
    post = get_object_or_404(Post, id=id)
    if action == 'unlike':
        post.users_like.remove(request.user)
    else:
        post.users_like.add(request.user)
        make_action(request.user, 'polubił', post)
    return JsonResponse({'status': 'ok'})

'''
def list(request, username=None):
    # list of posts :
    if username:  # for particular user
        user = get_user_model().objects.get(username=username)
        posts = Post.objects.filter(author=user)
        form = None
        choice = '-created'
    else:  # for all posts
        user = None
        posts = Post.objects.all()
        form = ChoiceOrderForm()  # form for choice ordering
        choice = '-created'  # default
        if 'choice' in request.GET:
            form = ChoiceOrderForm(request.GET)
            if form.is_valid():
                choice = form.cleaned_data['choice']
                posts = Post.objects.annotate(num_comments=Count(
                    'comments', distinct=True), num_likes=Count('users_like', distinct=True))
                posts = posts.order_by(choice)

    paginator = Paginator(posts, 3)
    page = request.GET.get('page', 1)

    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'content/list_ajax.html', {'section': 'blog', 'posts': posts})
    return render(request, 'content/list.html', {'section': 'blog', 'posts': posts, 'form': form, 'user': user, 'choice': choice})
'''

class CreatePost(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'content/post_create.html'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        new_post.save()
        make_action(self.request.user, "utworzył", new_post)
        return redirect(reverse('content:detail', kwargs={'slug':new_post.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        return context

'''
def create(request):
    if request.method == 'POST':
        form = NewPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post dodano')
            return redirect('content:list')
    else:
        form = NewPostForm()
    return render(request, 'content/post_create.html', {'section': 'blog', 'form': form})
'''

class UpdatePost(UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'content/post_edit.html'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        new_post.save()
        make_action(self.request.user, "edytował", new_post)
        return redirect(reverse('content:detail', kwargs={'slug':new_post.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        return context

'''
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = EditPostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            # save activity in logs
            make_action(request.user, "edytował", post)
            messages.success(request, 'ok')
            return redirect(post.get_absolute_url())
    else:
        form = EditPostForm(instance=post)
    return render(request, 'content/post_edit.html', {'section': 'blog', 'form': form})
'''

class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('content:list')

class DetailPost(DetailView):
    model = Post
    template_name = 'content/post_detail.html'
    form = NewCommentForm()

    def post(self, request, *args, **kwargs):
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = self.get_object()
            new_comment.save()
            make_action(self.request.user, 'skomentował', self.get_object())
            return redirect('.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comments.all()
        context['section'] = 'blog'
        context['form'] = self.form
        return context

'''
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()

    if request.method == "POST":
        # for adding new comment
        form = NewCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            make_action(request.user, 'skomentował', post) # save activity in logs
            post.hit_page(request.user) # function for increase hit page for post and user
            form = NewCommentForm(None)
    else:
        form = NewCommentForm()
        post.hit_page(request.user) 
    return render(request, 'content/post_detail.html', {'section': 'blog', 'post': post, 'form': form, 'comments': comments})
'''

