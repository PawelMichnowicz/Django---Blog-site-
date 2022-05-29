from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

# Create your models here.

class Action(models.Model):
    # model for saving user's acitvity
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='action')
    verb = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.user, self.verb, self.content_object)

    class Meta:
        ordering = ('-date',)




class Post(models.Model):
    # model for posts
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    title = models.CharField(max_length=30)
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50) 
    users_like = models.ManyToManyField(get_user_model(), related_name='likes', blank=True) 
    hits = models.PositiveIntegerField(default=0) #number of visit post

    class Meta:
        ordering = ('-date_create',)

    def unique_slug(instance, field_to_slug):
        # function for making unique slug for created post in save method
        model = instance.__class__
        while True:
            new_slug = slugify(field_to_slug + '-' + get_random_string(length=4))
            if not model.objects.filter(slug=new_slug).exists():
                return new_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.unique_slug(self.title)
            self.title = self.title.lower().capitalize()
        else:
            self.date_edit = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:detail", args=[self.slug])

    def __str__(self):
        return "{}: {} likes, {} comms".format(self.title, self.users_like.count(), self.comments.count())

    def hit_page(self, user, comment=False):
        # increase num of hits for user who vistited the posts, and for post that has visited
        self.hits += 1
        user.profile.num_of_hits += 1
        self.save()
        user.profile.save()


class Comment(models.Model):
    # model for coments
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_create',)


##########################################


