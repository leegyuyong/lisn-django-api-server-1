from django.urls import path
from . import views

urlpatterns = [
    path('token/google', views.views_token.api_token_google, name='api_token_google'),
    path('list/note/all', views.views_list.api_list_note_all, name='api_list_note_all'),
    path('list/note/trash', views.views_list.api_list_note_trash, name='api_list_note_trash'),
    path('note', views.views_note.api_note, name='api_note'),
    path('note/audio', views.views_audio.api_note_audio, name='api_note_audio'),
    path('note/trash', views.views_trash.api_note_trash, name='api_note_trash'),
    path('note/sentence', views.views_sentence.api_note_sentence, name='api_note_sentence'),
]