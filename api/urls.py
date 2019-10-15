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
    # directory 이동
    path('note/directory', views.views_directory.api_note_directory, name='api_note_directory'),
    # user의 directory list 반환
    path('list/directory', views.views_list.api_list_directory, name='api_list_directory'),
    # directory 생성, 수정, 삭제
    path('directory', views.views_directory.api_directory, name='api_directory'),
    # profile 정보
    path('profile', views.views_profile.api_profile, name='api_profile'),
    # 특정 directory의 note list 반환
    path('list/note', views.views_list.api_list_note, name='api_list_note'),
    # note 공유
    path('note/shared', views.views_share.api_note_shared, name='api_note_shared'),
    # 공유된 note list 반환
    path('list/note/shared', views.views_list.api_list_note_shared, name='api_list_note_shared'),
    # 공유된 user list 반환
    path('list/user/shared', views.views_list.api_list_user_shared, name='api_list_user_shared'),
    # directory+note 삭제
    path('directory/trash', views.views_trash.api_directory_trash, name='api_directory_trash'),
    # note 편집
    path('note/edited', views.views_edit.api_note_edited, name='api_note_edited'),
    path('search/title', views.views_search.api_search_title, name='api_search_title'),
    path('search/content', views.views_search.api_search_content, name='api_search_content'),
    path('search/sentence', views.views_search.api_search_sentence, name='api_search_sentence'),
    path('search/note/sentence', views.views_search.api_search_note_sentence, name='api_search_note_sentence'),
]