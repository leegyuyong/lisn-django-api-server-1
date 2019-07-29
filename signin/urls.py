from django.urls import path
from . import views

urlpatterns = [
    path('page', views.get_signin_page, name='get_signin_page'),
]