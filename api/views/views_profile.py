from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Audio, Sentence
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
    
    audio_usage = 0
    notes = Note.objects.filter(user_id=user_id)
    for note in notes:
        audios = Audio.objects.filter(note_id=note.id)
        for audio in audios:
            audio_usage = audio_usage + audio.length

    json_res['user_num_of_notes'] = len(notes)
    json_res['user_audio_usage'] = audio_usage

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