from django.urls import path
from . import views

urlpatterns = [
    path('mylist', views.mylist_html, name='mylist_html'),
    path('note', views.note_html, name='note_html'),
    path('audio', views.audio_stt, name='audio_stt'),
]