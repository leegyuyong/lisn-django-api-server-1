from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_main_page, name='get_main_page'),
]