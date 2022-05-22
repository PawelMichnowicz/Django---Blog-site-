from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User 
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F
# Create your views here.

from .models import Tweet, Action
from .forms import NewTweetForm, NewCommentForm, ChoiceOrderForm, EditTweetForm, ShowTweet, ShowUsers
from .utils import make_action

def dashboard(request):
    # view with top 18 activity logs
    actions = Action.objects.all()[:18]
    return render(request, 'content/dashboard.html',{'section':'main', 'actions':actions})

def dash_users_ajax(request):
    # ajax view source for top users
    users = None
    form = ShowUsers() # form for choice param
    choice = None
    if 'choice' in request.GET:
        form = ShowUsers(request.GET)
        if form.is_valid():
            choice = form.cleaned_data['choice'] # choice from ShowUsers form 
            users = User.objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count('likes', distinct=True), hits=F('profile__num_of_hits')) # addding stats of number of comments/likes/hits to users
            users = users.order_by(choice)[:5] # ordering

    return render(request, 'content/dash_users_ajax.html', {'section':'main', 'users':users, 'form':form, "choice":choice})

def dash_posts_ajax(request):
    # ajax view source for top posts
    posts = None
    form = ShowTweet()
    choice = None
    choice_label = None
    if 'choice' in request.GET:
        form = ShowTweet(request.GET)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            posts = Tweet.objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count('users_like', distinct=True)) # addding stats of number of comments/likes/hits to users
            posts = posts.order_by(choice)[:5]



    return render(request, 'content/dash_posts_ajax.html', {'section':'main', 'posts':posts, 'form':form, "choice":choice,})


def list(request, username=None):
    # list of posts : 
    if username: # for particular user
        user = User.objects.get(username=username)
        posts = Tweet.objects.filter(author=user)
        form = None
        choice = '-created'
    else: # for all posts
        user = None
        posts = Tweet.objects.all()
        form = ChoiceOrderForm() # form for choice ordering 
        choice = '-created' # default
        if 'choice' in request.GET:
            form = ChoiceOrderForm(request.GET)
            if form.is_valid():
                choice = form.cleaned_data['choice']
                posts = Tweet.objects.annotate(num_comments=Count('comments', distinct=True), num_likes=Count('users_like', distinct=True))
                posts = posts.order_by(choice)

    paginator = Paginator(posts, 3) 
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest': #if request.is_ajax():
        return render(request, 'content/list_ajax.html', {'section':'blog', 'posts':posts})
    return render(request, 'content/list.html', {'section':'blog', 'posts':posts, 'form':form, 'user':user, 'choice':choice})

def create(request):
    if request.method == 'POST':
        form = NewTweetForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post dodano')
            return redirect('content:list')
    else:
        form = NewTweetForm()
    return render(request, 'content/post_create.html', {'section':'blog', 'form':form})

def post_edit(request, slug):
    post = get_object_or_404(Tweet, slug=slug)
    if request.method == 'POST':
        form = EditTweetForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            make_action(request.user, "edytował", post) # save activity in logs
            messages.success(request, 'ok')
            return redirect(post.get_absolute_url())
    else:
        form = EditTweetForm(instance=post)
    return render(request, 'content/post_edit.html', {'section':'blog', 'form':form})

def post_detail(request, slug):
    post = get_object_or_404(Tweet, slug=slug)
    comments = post.comments.all()
    post.hit_page(request.user) # function for increase hit page for post and user #1 #+1

    if request.method == "POST":
        # for adding new comment
        form = NewCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            make_action(request.user, 'skomentował', post) # save activity in logs #2
            post.hit_page(request.user, comment=True)   
            form = NewCommentForm(None)
    else:
        form = NewCommentForm()
    return render(request, 'content/post_detail.html', {'section':'blog', 'post':post, 'form':form, 'comments':comments})

@require_POST
def post_like(request):
    # ajax view for adding like
    id = request.POST.get('id')
    action = request.POST.get('action')
    post = get_object_or_404(Tweet, id=id)
    if action == 'unlike':
        post.users_like.remove(request.user)
    else:
        post.users_like.add(request.user)
        make_action(request.user, 'polubił', post)
    return JsonResponse({'status':'ok'})


