from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.utils import timezone

from api.models import Note, Audio
from api.s3_client import upload_file_to_s3, create_presigned_url_s3

def upload_audio_data(request):
    request_param = request.POST
    note_id = int(request.POST.get('note_id'))
    note = Note.objects.get(id=note_id)
    user_id = note.user.id
    
    note.updated_at = timezone.now()
    note.save()
    
    audio = Audio.objects.create(
        note_id=note_id,
        user_id=user_id
    )

    audio_data = request.FILES['audio_data']
    upload_file_to_s3(audio_data, settings.AWS_S3_MEDIA_DIR + str(audio.id) + '.webm')
    
    json_res = dict()
    json_res['audio_id'] = audio.id
    
    log(request=request, status_code=201, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res, status=201)

def get_audio_data_url(request):
    request_param = request.GET
    audio_id = int(request.GET.get('audio_id'))
    audio = Audio.objects.get(id=audio_id)
    
    json_res = dict()
    # data_url -> audio_url
    json_res['audio_url'] = create_presigned_url_s3(settings.AWS_S3_MEDIA_DIR + str(audio.id) + '.webm')

    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def api_note_audio(request):
    try:
        if request.method == 'GET':
            return get_audio_data_url(request)
        elif request.method == 'POST':
            return upload_audio_data(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)