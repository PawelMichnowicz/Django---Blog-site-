from django.contrib import admin
from .models import Post, Comment, Action

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'text', 'title','date_create', 'date_edit']
    list_editable = ['text', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Action._meta.get_fields()]

