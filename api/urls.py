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
    path('list/note', views.views_directory.api_directory_note_list, name='api_directory_note_list'),         # user의 특정 directory의 note list 반환(trash 제외)
    path('list/directory', views.views_directory.api_directory_list, name='api_directory_list'),              # user의 directory list 반환
    path('directory', views.views_directory.api_directory, name='api_directory'),                             # directory 생성, 수정, 삭제
    path('note/directory', views.views_directory.api_note_move, name="api_note_move")                         # directory 이동
]