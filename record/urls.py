from django.urls import path
from . import views

urlpatterns = [
    path('list', views.get_list, name='get_list'),
    path('note', views.manipulate_note, name='manipulate_note'),
    path('audio', views.save_audio, name='save_audio'),
    path('sentence', views.manipulate_sentence, name='manipulate_sentence'),
]