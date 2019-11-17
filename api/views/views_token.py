from log import log
import sys
import datetime
import jwt

from google.oauth2 import id_token
from google.auth.transport import requests

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from api.models import User, Note, Audio, Sentence, Directory
from api.utils import coerce_to_post
from config.settings import JWT_SECRET_KEY
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id
from api.s3_client.s3_client import copy_file_to_s3
from api.es_client.es_client import es

CLIENT_ID = '935445294329-t38oc4vmt9l5sokr34h8ueap63dfq4hi.apps.googleusercontent.com'

def make_tutorial(user):
    directory = Directory.objects.create(
        user_id=user.id,
        name=user.name+'님의 폴더'
    )

    note = Note.objects.create(
        user_id=user.id,
        directory_id=directory.id,
        title='튜토리얼 노트',
        created_at=timezone.now(),
        updated_at=timezone.now(),
        deleted_at=timezone.now(),
        content='<h2>\uc774 \ub178\ud2b8\ub294 \ud29c\ud1a0\ub9ac\uc5bc \ub178\ud2b8\uc785\ub2c8\ub2e4.                                                              </h2>\
        <p></p><p>\uc704\uc758 \uc7ac\uc0dd\ubc84\ud2bc\uc744 \ub20c\ub7ec\ubcf4\uc138\uc694.</p><p></p>\
        <p>\ubb38\uc7a5\uc744 \ud074\ub9ad\ud558\uba74 \ud574\ub2f9 \ubd80\ubd84\ubd80\ud130 \uc7ac\uc0dd\ub429\ub2c8\ub2e4.</p><p></p>\
        <p>\uc790\uc2e0\ub9cc\uc758 \ubcf4\uc774\uc2a4 \ub178\ud2b8\ub97c \ub9cc\ub4e4\uace0 \uc2f6\ub2e4\uba74,\
         \uc9c0\uae08 \ubc14\ub85c <strong>\uc0c8 \ub178\ud2b8</strong>\ub97c \uc791\uc131\ud574 \ubcf4\uc138\uc694!</p>',
        is_trash=False
    )
    es_document = dict()
    es_document['note_id'] = note.id
    es_document['user_id'] = note.user.id
    es_document['title'] = note.title
    es_document['content'] = note.content
    es.create(index='note', body=es_document, id=note.id)

    audio = Audio.objects.create(
        note_id=note.id,
        user_id=user.id,
        length=0
    )
    copy_file_to_s3(settings.AWS_S3_MEDIA_DIR + '0.webm', settings.AWS_S3_MEDIA_DIR + str(audio.id)+'.webm')

    sentence = Sentence.objects.create(
        index=0,
        audio_id=audio.id,
        user_id=user.id,
        started_at=0,
        ended_at=3388,
        content='\uc774 \ub178\ud2b8\ub294 \ud29c\ud1a0\ub9ac\uc5bc \ub178\ud2b8\uc785\ub2c8\ub2e4'
    )
    es_document = dict()
    es_document['sentence_id'] = sentence.id
    es_document['note_id'] = audio.note.id
    es_document['user_id'] = audio.user.id
    es_document['content'] = sentence.content
    es.create(index='sentence', body=es_document, id=sentence.id)
    sentence = Sentence.objects.create(
        index=1,
        audio_id=audio.id,
        user_id=user.id,
        started_at=2891,
        ended_at=6581,
        content='\uc774 \ubb38\uc7a5\uc744 \ud074\ub9ad\ud574\ubcf4\uc138\uc694'
    )
    es_document = dict()
    es_document['sentence_id'] = sentence.id
    es_document['note_id'] = audio.note.id
    es_document['user_id'] = audio.user.id
    es_document['content'] = sentence.content
    es.create(index='sentence', body=es_document, id=sentence.id)
    sentence = Sentence.objects.create(
        index=2,
        audio_id=audio.id,
        user_id=user.id,
        started_at=6691,
        ended_at=12493,
        content=' \ud074\ub9ad\ud55c \ubb38\uc7a5\ubd80\ud130 \ub179\uc74c \ub0b4\uc6a9\uc744 \uc7ac\uc0dd\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4'
    )
    es_document = dict()
    es_document['sentence_id'] = sentence.id
    es_document['note_id'] = audio.note.id
    es_document['user_id'] = audio.user.id
    es_document['content'] = sentence.content
    es.create(index='sentence', body=es_document, id=sentence.id)
    sentence = Sentence.objects.create(
        index=3,
        audio_id=audio.id,
        user_id=user.id,
        started_at=11583,
        ended_at=16112,
        content=' \uc9c0\uae08 \ubc14\ub85c \uc0c8 \ub178\ud2b8\ub97c \uc791\uc131\ud574 \ubcf4\uc138\uc694'
    )
    es_document = dict()
    es_document['sentence_id'] = sentence.id
    es_document['note_id'] = audio.note.id
    es_document['user_id'] = audio.user.id
    es_document['content'] = sentence.content
    es.create(index='sentence', body=es_document, id=sentence.id)
    print('\n4\n')

def get_token(request):
    token = request.POST.get('google_token')
    user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

    if user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return HttpResponse(status=400)
    
    user_name = user_info['name']
    user_email = user_info['email']
    user_picture_url = user_info['picture']
    user_language = 'ko-KR'
    user_list = User.objects.filter(email=user_email)

    if len(user_list) == 0:
        user = User.objects.create(name=user_name, email=user_email, picture_url=user_picture_url, language=user_language)

        # elasticsearch document create
        es_document = dict()
        es_document['name'] = user_name
        es_document['email'] = user_email
        es_document['picture_url'] = user_picture_url
        es_document['language'] = 'ko-KR'
        es.create(index='user', body=es_document, id=user.id)

        make_tutorial(user)
    else:
        user = user_list[0]
        user.picture_url = user_picture_url
        user.save()
    
    payload = dict()
    payload['user_id'] = user.id
    payload['email'] = user.email
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*24)
    
    byte_access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    access_token = byte_access_token.decode('utf-8')

    json_res = dict()
    json_res['user_id'] = user.id
    json_res['access_token'] = access_token

    return JsonResponse(json_res, status=201)

@log
def api_token_google(request):
    try:
        if request.method == 'POST':
            return get_token(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)