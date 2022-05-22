from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.utils import timezone

from .models import Action




def make_action(user, verb, content_object):
    now = timezone.now()
    last_minute = now - timezone.timedelta(seconds=60)

    if not Action.objects.filter(user=user, verb=verb, object_id=content_object.id, date__gte=last_minute):
        new_action = Action(user=user, verb=verb, content_object=content_object)
        new_action.save()
        