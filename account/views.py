from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User 

from . import forms
from content.models import Tweet

# Create your views here.


def user_detail(request, username):
    # info about choosen user (number of posts/comments)
    user = User.objects.get(username=username)
    return render(request, 'account/user_detail.html', {'user':user})

def detail(request):
    # view for change image avatar
    user = request.user
    if request.method == "POST":
        image_form = forms.ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if image_form.is_valid(): 
            image_form.save()
            messages.success(request, 'Zaktualizowano')
        else:
            messages.error(request, 'Nie Zaktualizowano')
    else:
        image_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/detail.html', {'user':user, 'image_form':image_form})

def register(request):
    # view for registration
    if request.method == 'POST':
        user_form = forms.RegisterForm(request.POST)
        profile_form = forms.ProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():

            cd = user_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.set_password(cd['password'])

            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user

            new_user.save()
            new_profile.save()

            login(request, new_user)
            return render(request, 'content/dashboard.html', {'section':'main','user':new_user})
    else:
        user_form = forms.RegisterForm()
        profile_form = forms.ProfileForm()
    return render(request, 'account/register.html', {'user_form':user_form, 'profile_form':profile_form})




