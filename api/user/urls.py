from django.urls import path
from . import views

urlpatterns = [
    path('oauth/google/user', views.signin, name='signin'),
    path('token', views.delete_token, name='delete_token'),
]