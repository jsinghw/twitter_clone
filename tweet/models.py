from django.db import models
from django.utils import timezone
from twitter_user.models import Profile


# Create your models here.
class Tweet(models.Model):
    content = models.TextField(max_length=140)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['content']
