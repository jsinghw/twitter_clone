from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from twitter_user.models import Profile, Follow


# Register your models here.
admin.site.register(Profile, UserAdmin)
admin.site.register(Follow)
