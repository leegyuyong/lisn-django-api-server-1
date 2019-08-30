from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import Audio, Sentence

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

def api_note_sentence(request):
    try:
        if request.method == 'POST':
            return create_sentence(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)