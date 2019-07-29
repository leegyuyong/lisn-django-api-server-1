from django.urls import path
from . import views

urlpatterns = [
    path('mylist', views.get_mylist_page, name='get_mylist_page'),
    path('note', views.manipulate_note, name='manipulate_note'),
    path('audio', views.audio_file_save, name='audio_file_save'),
]