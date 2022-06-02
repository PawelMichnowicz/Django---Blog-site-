from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, CreateView, TemplateView

from . import forms




# def user_detail(request, username):
#     # info about choosen user (number of posts/comments)
#     user = get_user_model().objects.get(username=username)
#     return render(request, 'account/user_detail.html', {'user':user})

class UserDetail(DetailView):
    template_name = 'account/user_detail.html'
    model = get_user_model()

    def username(self):
        return self.kwargs['username']
    
    def get_object(self, queryset=None):
        return get_user_model().objects.get(username=self.username())


class UserSettings(DetailView):
    template_name = 'account/detail.html'
    model = get_user_model()
    image_form = forms.ProfileEditForm()

    def get_object(self, queryset=None):
        return get_user_model().objects.get(username=self.request.user.username)

    def post(self, request, *args, **kwargs): 
        image_form = forms.ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if image_form.is_valid(): 
            image_form.save()
        return render(request, 'account/detail.html', {'user':self.request.user, 'image_form':image_form})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.image_form
        return context


class Register(TemplateView):
    template_name = 'account/register.html'

    def post(self, request, *args, **kwargs): 
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = forms.RegisterForm()
        context['profile_form'] = forms.ProfileForm()
        return context





