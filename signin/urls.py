from django.urls import path
from . import views

urlpatterns = [
    path('oauth/google', views.oauth_google, name='oauth_google'),
]