from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from django.contrib import admin
from .models import Tweet, Comment, Action

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'text', 'title','date_create', 'date_edit']
    list_editable = ['text', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Action._meta.get_fields()]

