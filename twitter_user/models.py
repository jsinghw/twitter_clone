from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Profile(AbstractUser):
    handle = models.CharField(max_length=50, null=True)
    followers = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='following_user'
    )
    following = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='following_other'
    )
    REQUIRED_FIELDS = ['handle']

    def __str__(self):
        return self.handle

    # @property
    # def followers(self):
    #     return Profile.objects.filter(follow_user=self.handle).count()
    #
    # @property
    # def following(self):
    #     return Follow.objects.filter(user=self.handle).count()
