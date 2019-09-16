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
    path('note/directory', views.views_directory.api_note_directory, name='api_note_directory'),                         # directory 이동
    path('list/directory', views.views_list.api_list_directory, name='api_list_directory'),              # user의 directory list 반환
    path('directory', views.views_directory.api_directory, name='api_directory'),                             # directory 생성, 수정, 삭제
    path('profile', views.views_profile.api_profile, name='api_profile'),                                   # profile 정보
    path('list/note', views.views_list.api_list_note, name='api_list_note'),                                # 특정 directory의 note list 반환
    path('note/shared', views.views_share.api_note_shared, name='api_note_shared'),                         # note 공유
    path('list/note/shared', views.views_list.api_list_note_shared, name='api_list_note_shared'),                     # 공유된 note list 반환
    path('list/user/shared', views.views_list.api_list_user_shared, name='api_list_user_shared'),                     # 공유된 user list 반환
    #path('note/posted', views.views_post.api_note_posted, name='api_note_posted'),                          # note posting
    path('directory/trash', views.views_trash.api_directory_trash, name='api_directory_trash'),          # directory+note 삭제
]