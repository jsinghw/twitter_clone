from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from tweet.forms import AddTweetForm
from tweet.models import Tweet
from notification.models import Notification
from twitter_user.models import Profile
import re


@login_required
def add_tweet(request):
    html = 'add_tweet.html'
    notifcation_count = Notification.objects.filter(user=request.user).count()
    if request.method == "POST":
        form = AddTweetForm(request.POST)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.profile = request.user
            new_tweet.save()

# check to see if there is any mentions and add notification if there is
            reg = re.compile(r'(.*)(@\S*)')
            m = reg.match(new_tweet.content)
            if m:
                if Profile.objects.filter(handle=m[2][1:]):
                    new_notification = Notification(
                        user=Profile.objects.get(handle=m[2][1:]),
                        tweet=new_tweet
                    )
                    new_notification.save()

        return HttpResponseRedirect(reverse('homepage'))
    form = AddTweetForm()
    return render(
        request,
        html,
        {'form': form, 'notifcation_count': notifcation_count}
    )


def detail_tweet(request, id):
    html = 'detail_tweet.html'
    data = Tweet.objects.get(id=id)
    if request.user.is_authenticated:
        notifcation_count = Notification.objects.filter(user=request.user).count()
        return render(
            request,
            html,
            {'data': data, 'notifcation_count': notifcation_count}
        )
    else:
        return render(
            request,
            html,
            {'data': data}
        )
