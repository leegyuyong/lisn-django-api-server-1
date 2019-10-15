from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import Audio, Sentence
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_sentence_id_shared, auth_sentence_id_edit
from api.utils import coerce_to_post
from api.es_client.es_client import es

@auth_sentence_id_shared
def get_sentence_info(request):
    sentence_id = int(request.GET.get('sentence_id'))
    sentence = Sentence.objects.get(id=sentence_id)

    json_res = dict()
    json_res['audio_id'] = sentence.audio.id
    json_res['index'] = sentence.index
    json_res['started_at'] = sentence.started_at
    json_res['ended_at'] = sentence.ended_at
    json_res['content'] = sentence.content

    return JsonResponse(json_res)

@auth_audio_id
def create_sentence(request):
    index = int(request.POST.get('index'))
    audio_id = int(request.POST.get('audio_id'))
    started_at = int(request.POST.get('started_at'))
    ended_at = int(request.POST.get('ended_at'))
    content = str(request.POST.get('content'))
    audio = Audio.objects.get(id=audio_id)
    user_id = audio.user.id
    
    sentence = Sentence.objects.create(
        index=index,
        audio_id=audio_id,
        user_id=user_id,
        started_at=started_at,
        ended_at=ended_at,
        content=content
    )
    json_res = dict()
    json_res['sentence_id'] = sentence.id
    
    # elasticsearch document create
    es_document = dict()
    es_document['sentence_id'] = sentence.id
    es_document['note_id'] = audio.note.id
    es_document['user_id'] = audio.user.id
    es_document['content'] = sentence.content
    es.create(index='sentence', body=es_document, id=sentence.id)

    return JsonResponse(json_res, status=201)

@auth_sentence_id_shared
@auth_sentence_id_edit
def update_sentence(request):
    coerce_to_post(request)

    sentence_id = int(request.PUT.get('sentence_id'))
    content = str(request.PUT.get('content'))
    sentence = Sentence.objects.get(id=sentence_id)
    
    sentence.content = content
    sentence.save()

    # elasticsearch document update
    es_document = dict()
    es_document['content'] = sentence.content
    es.update(index='sentence', body={'doc':es_document}, id=sentence.id)

    return HttpResponse(status=200)

@auth_sentence_id_shared
@auth_sentence_id_edit
def delete_sentence(request):
    coerce_to_post(request)

    sentence_id = int(request.DELETE.get('sentence_id'))
    sentence = Sentence.objects.get(id=sentence_id)

    sentence.delete()
    
    # elasticsearch document delete
    es.delete(index='sentence', id=sentence_id)

    return HttpResponse(status=200)

@log
def api_note_sentence(request):
    try:
        if request.method == 'GET':
            return get_sentence_info(request)
        elif request.method == 'POST':
            return create_sentence(request)
        elif request.method == 'PUT':
            return update_sentence(request)
        elif request.method == 'DELETE':
            return delete_sentence(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)