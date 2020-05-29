from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notification.models import Notification
from twitter_user.models import Profile


@login_required
def notifications_view(request, handle):
    html = 'notification.html'
    notifcation_count = Notification.objects.filter(user=request.user).count()
    tweets = Notification.objects.filter(
        user=Profile.objects.get(handle=handle))

    for x in tweets:
        x.delete()

    return render(
        request,
        html,
        {'tweets': tweets, 'notifcation_count': notifcation_count}
    )
