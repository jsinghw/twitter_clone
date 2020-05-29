from django.contrib.auth.forms import UserCreationForm
from twitter_user.models import Profile


class SignUpForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ('username', 'handle', 'password1', 'password2', )
