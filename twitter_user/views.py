from notification.models import Notification
from tweet.models import Tweet
from twitter_user.models import Profile
from twitter_user.forms import SignUpForm
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def index(request):
    data = Profile.objects.get(id=request.user.id)
    tweet_count = Tweet.objects.filter(
        profile=request.user).count()
    notifcation_count = Notification.objects.filter(user=request.user).count()

    feed = Tweet.objects.filter(
        profile=request.user)
    follower_list = Profile.objects.filter(following_other=request.user)
    for x in follower_list:
        feed |= Tweet.objects.filter(profile=x.id)
    feed = feed.order_by('-date_created')

    return render(
        request,
        'index.html',
        {
            'data': data,
            'tweet_count': tweet_count,
            'feed': feed,
            'notifcation_count': notifcation_count
        }
    )


class AltIndex(LoginRequiredMixin, View):
    def get(self, request):
        data = Profile.objects.get(id=request.user.id)
        tweet_count = Tweet.objects.filter(
            profile=request.user).count()
        notifcation_count = Notification.objects.filter(user=request.user).count()

        feed = Tweet.objects.filter(
            profile=request.user)
        follower_list = Profile.objects.filter(following_other=request.user)
        for x in follower_list:
            feed |= Tweet.objects.filter(profile=x.id)
        feed = feed.order_by('-date_created')

        return render(
            request,
            'index.html',
            {
                'data': data,
                'tweet_count': tweet_count,
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


class AltSignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
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
        profile=Profile.objects.get(handle=handle)
    ).order_by('-date_created')

    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(user=request.user).count()
        if Profile.objects.filter(handle=request.user.handle, following_user=data.id):
            following = True
        else:
            following = False
        return render(
            request,
            html,
            {'data': data,
             'tweets': tweets,
             'notifcation_count': notification_count,
             'following': following
             }
        )
    else:
        return render(
            request,
            html,
            {'data': data,
             'tweets': tweets
             }
        )


@login_required
def follow(request, handle):
    url = reverse('profile', kwargs={'handle': handle})
    new_follower = Profile.objects.get(
        handle=handle)
    new_follower.following_other.add(request.user)
    new_follower.save()

    new_following = Profile.objects.get(
        handle=request.user.handle)
    new_following.following_user.add(
        Profile.objects.get(handle=handle))
    new_following.save()
    return HttpResponseRedirect(url)


class AltFollow(LoginRequiredMixin, View):
    def get(self, request, handle):
        url = reverse('profile', kwargs={'handle': handle})
        new_follower = Profile.objects.get(
            handle=handle)
        new_follower.following_other.add(request.user)
        new_follower.save()

        new_following = Profile.objects.get(
            handle=request.user.handle)
        new_following.following_user.add(
            Profile.objects.get(handle=handle))
        new_following.save()
        return HttpResponseRedirect(url)


@login_required
def unfollow(request, handle):
    url = reverse('profile', kwargs={'handle': handle})
    stop_follower = Profile.objects.get(handle=handle)
    stop_follower.following_other.remove(request.user)

    stop_following = Profile.objects.get(
        handle=request.user.handle)
    stop_following.following_user.remove(
        Profile.objects.get(handle=handle))
    return HttpResponseRedirect(url)
