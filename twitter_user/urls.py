from django.urls import path
from twitter_user import views

urlpatterns = [
    path('', views.AltIndex.as_view(), name='homepage'),
    path('signup/', views.AltSignUpView.as_view()),
    path('user/<str:handle>/', views.profile_page, name='profile'),
    path('user/follow/<str:handle>/', views.AltFollow.as_view()),
    path('user/unfollow/<str:handle>', views.unfollow)
]
