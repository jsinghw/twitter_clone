from django.urls import path
from tweet import views

urlpatterns = [
    path('tweet/add/', views.add_tweet),
    path('tweet/detail/<int:id>/', views.detail_tweet)
]
