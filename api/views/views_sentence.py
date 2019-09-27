from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import Audio, Sentence
from api.utils import coerce_to_post

def get_sentence_info(request):
    request_param = request.GET
    sentence_id = int(request.GET.get('sentence_id'))
    sentence = Sentence.objects.get(id=sentence_id)

    json_res = dict()
    json_res['audio_id'] = sentence.audio.id
    json_res['index'] = sentence.index
    json_res['started_at'] = sentence.started_at
    json_res['ended_at'] = sentence.ended_at
    json_res['content'] = sentence.content
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def create_sentence(request):
    request_param = request.POST
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
    
    log(request=request, status_code=201, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res, status=201)

def update_sentence(request):
    coerce_to_post(request)
    request_param = request.PUT

    sentence_id = int(request.PUT.get('sentence_id'))
    content = str(request.PUT.get('content'))
    sentence = Sentence.objects.get(id=sentence_id)
    
    sentence.content = content
    sentence.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def delete_sentence(request):
    coerce_to_post(request)
    request_param = request.DELETE

    sentence_id = int(request.DELETE.get('sentence_id'))
    sentence = Sentence.objects.get(id=sentence_id)

    sentence.delete()
    
    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

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
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)