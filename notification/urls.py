from django.urls import path
from notification import views

urlpatterns = [
    path('user/<str:handle>/notifications', views.notifications_view)
]
