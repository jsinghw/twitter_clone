from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Profile(AbstractUser):
    handle = models.CharField(max_length=50, null=True)

    REQUIRED_FIELDS = ['handle']

    def __str__(self):
        return self.handle

    # @property
    # def followers(self):
    #     return Follow.objects.filter(follow_user=self.handle).count()
    #
    # @property
    # def following(self):
    #     return Follow.objects.filter(user=self.handle).count()


class Follow(models.Model):
    user = models.ForeignKey(
        Profile, related_name='follows', on_delete=models.CASCADE
    )
    follow_user = models.ForeignKey(
        Profile, related_name='follow_user', on_delete=models.CASCADE
    )
