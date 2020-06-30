from django.urls import path
from tweet import views

urlpatterns = [
    path('tweet/add/', views.AltAddTweet.as_view()),
    path('tweet/detail/<int:id>/', views.detail_tweet)
]
