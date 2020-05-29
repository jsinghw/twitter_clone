from django.urls import path
from twitter_user import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('signup/', views.signup_view),
    path('user/<str:handle>/', views.profile_page, name='profile'),
    path('user/follow/<str:handle>/', views.follow),
    path('user/unfollow/<str:handle>', views.unfollow)
]
