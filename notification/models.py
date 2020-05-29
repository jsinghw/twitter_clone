from django.db import models
from twitter_user.models import Profile
from tweet.models import Tweet


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
