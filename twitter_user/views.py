from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from twitter_user.forms import SignUpForm
from twitter_user.models import Profile, Follow
from tweet.models import Tweet
from notification.models import Notification

# Create your views here.
@login_required
def index(request):
    tweet_count = Tweet.objects.filter(
        profile=request.user).count()
    following_count = Follow.objects.filter(user=request.user).count()
    followers_count = Follow.objects.filter(follow_user=request.user).count()
    notifcation_count = Notification.objects.filter(user=request.user).count()

    feed = Tweet.objects.filter(
        profile=request.user)
    follower_list = Follow.objects.filter(user=request.user)
    for x in follower_list:
        feed |= Tweet.objects.filter(profile=x.follow_user)
    feed = feed.order_by('-date_created')

    return render(
        request,
        'index.html',
        {
            'tweet_count': tweet_count,
            'following_count': following_count,
            'followers_count': followers_count,
            'feed': feed,
            'notifcation_count': notifcation_count
        }
    )


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def profile_page(request, handle):
    html = 'profile_page.html'
    data = Profile.objects.get(handle=handle)
    tweets = Tweet.objects.filter(
        profile=Profile.objects.get(handle=handle)).order_by('-date_created')
    tweet_count = tweets.count()
    following_count = Follow.objects.filter(
        user=Profile.objects.get(handle=handle)).count()
    followers_count = Follow.objects.filter(
        follow_user=Profile.objects.get(handle=handle)).count()
    if request.user.is_authenticated:
        if Follow.objects.filter(
                user=request.user, follow_user=Profile.objects.get(handle=handle)):
            notifcation_count = Notification.objects.filter(user=request.user).count()
            following = True
        else:
            following = False
    if request.user.is_authenticated:
        return render(
            request,
            html,
            {
                'data': data,
                'tweets': tweets,
                'tweet_count': tweet_count,
                'following': following,
                'following_count': following_count,
                'followers_count': followers_count,
                'notifcation_count': notifcation_count
            })
    else:
        return render(
            request,
            html,
            {
                'data': data,
                'tweets': tweets,
                'tweet_count': tweet_count,
                'following_count': following_count,
                'followers_count': followers_count
            })


@login_required
def follow(request, handle):
    url = reverse('profile', kwargs={'handle': handle})
    new_follow = Follow(
        user=request.user, follow_user=Profile.objects.get(handle=handle)
    )
    new_follow.save()
    return HttpResponseRedirect(url)


@login_required
def unfollow(request, handle):
    url = reverse('profile', kwargs={'handle': handle})
    stop_follow = Follow.objects.filter(
        user=request.user, follow_user=Profile.objects.get(handle=handle))
    stop_follow.delete()
    return HttpResponseRedirect(url)
