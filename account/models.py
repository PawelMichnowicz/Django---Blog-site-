from django.db import models

from django.contrib.auth import get_user_model


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'avatars/{}.{}'.format(instance.user.username, extension)

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile') # relation one-to-one with django's User model
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_location, blank=True, default='def_avatar/davatar.png') # avatar
    num_of_hits = models.PositiveIntegerField(default=10) # number of visiting posts
    






