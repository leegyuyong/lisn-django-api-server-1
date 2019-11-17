from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Audio, Sentence, Share
from api.utils import coerce_to_post
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id
from api.s3_client.s3_client import delete_file_to_s3
from api.es_client.es_client import es

@auth_user_id
def get_profile_info(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    
    json_res = dict()
    json_res['user_name'] = user.name
    json_res['user_email'] = user.email
    json_res['user_picture_url'] = user.picture_url
    json_res['user_language'] = user.language
    json_res['user_language_stt'] = user.language_stt

    return JsonResponse(json_res)

@auth_user_id
def delete_user(request):
    coerce_to_post(request)
    user_id = int(request.DELETE.get('user_id'))
    user = User.objects.get(id=user_id)

    notes = Note.objects.filter(user_id=user.id)
    for note in notes:
        # delete audio files
        audios = Audio.objects.filter(note_id=note.id)
        for audio in audios:
            delete_file_to_s3(settings.AWS_S3_MEDIA_DIR + str(audio.id) + '.webm')
            # elasticsearch document delete
            sentences = Sentence.objects.filter(audio_id=audio.id)
            for sentence in sentences:
                es.delete(index='sentence', id=sentence.id)
        
        # elasticsearch document delete
        es.delete(index='note', id=note.id)

    es.delete(index='user', id=user.id)
    user.delete()
    
    return HttpResponse(status=200)

@auth_user_id
def get_usage_info(request):
    user_id = int(request.GET.get('user_id'))

    audio_usage = 0
    notes = Note.objects.filter(user_id=user_id, is_trash=False)
    for note in notes:
        audios = Audio.objects.filter(note_id=note.id)
        for audio in audios:
            audio_usage = audio_usage + audio.length

    shared = len(Share.objects.filter(user_id=user_id))
    sharing = 0
    for note in notes:
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            sharing = sharing + 1

    json_res = dict()
    json_res['user_num_of_notes'] = len(notes)
    json_res['user_audio_usage'] = audio_usage
    json_res['user_num_of_shared'] = shared
    json_res['user_num_of_sharing'] = sharing

    return JsonResponse(json_res)

def get_status(request):
    users = User.objects.all()
    notes = Note.objects.all()
    audios = Audio.objects.all()
    sentences = Sentence.objects.all()

    json_res = dict()
    json_res['num_of_users'] = len(users)
    json_res['num_of_notes'] = len(notes)
    json_res['num_of_audios'] = len(audios)
    json_res['num_of_sentences'] = len(sentences)

    return JsonResponse(json_res)

@auth_user_id
def get_language(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)

    json_res = dict()
    json_res['user_language'] = user.language
    
    return JsonResponse(json_res)

@auth_user_id
def change_language(request):
    coerce_to_post(request)
    user_id = int(request.PUT.get('user_id'))
    language = request.PUT.get('language')
    user = User.objects.get(id=user_id)

    user.language = language
    user.save()

    es_document = dict()
    es_document['language'] = language
    es.update(index='user', body={'doc':es_document}, id=user.id)
    
    return HttpResponse(status=200)

@auth_user_id
def get_language_stt(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)

    json_res = dict()
    json_res['user_language_stt'] = user.language_stt
    
    return JsonResponse(json_res)

@auth_user_id
def change_language_stt(request):
    coerce_to_post(request)
    user_id = int(request.PUT.get('user_id'))
    language = request.PUT.get('language')
    user = User.objects.get(id=user_id)

    user.language_stt = language
    user.save()
    
    return HttpResponse(status=200)

@log
def api_profile(request):
    try:
        if request.method == 'GET':
            return get_profile_info(request)
        elif request.method == 'DELETE':
            return delete_user(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_profile_usage(request):
    try:
        if request.method == 'GET':
            return get_usage_info(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_profile_language(request):
    try:
        if request.method == 'GET':
            return get_language(request)
        elif request.method == 'PUT':
            return change_language(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_profile_language_stt(request):
    try:
        if request.method == 'GET':
            return get_language_stt(request)
        elif request.method == 'PUT':
            return change_language_stt(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_profile_status(request):
    try:
        if request.method == 'GET':
            return get_status(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)