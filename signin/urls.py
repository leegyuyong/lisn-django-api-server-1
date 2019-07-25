from django.urls import path
from . import views

urlpatterns = [
    path('page', views.signin_html, name='signin_html'),
]