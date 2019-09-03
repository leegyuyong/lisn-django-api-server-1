from log import log
import sys
import datetime

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.utils import timezone

from api.models import Note, Audio, Sentence
from api.utils import coerce_to_post
from api.s3_client import delete_file_to_s3

def get_note_info(request):
    request_param = request.GET
    note_id = int(request.GET.get('note_id'))
    note = Note.objects.get(id=note_id)

    json_res = dict()
    json_res['note_id'] = note.id
    json_res['title'] = note.title
    json_res['content'] = note.content
    json_res['started_at'] = note.started_at
    json_res['ended_at'] = note.ended_at
    json_res['audios'] = []

    audios = Audio.objects.filter(note_id=note_id).order_by('id')
    for audio in audios:
        json_audio = dict()
        json_audio['audio_id'] = audio.id
        json_audio['sentences'] = []

        sentences = Sentence.objects.filter(audio_id=audio.id).order_by('index')
        for sentence in sentences:
            json_sentence = dict()
            json_sentence['sentence_id'] = sentence.id
            json_sentence['started_at'] = sentence.started_at
            json_sentence['ended_at'] = sentence.ended_at
            json_sentence['content'] = sentence.content
            json_audio['sentences'].append(json_sentence)

        json_res['audios'].append(json_audio)
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def create_note(request):
    request_param = request.POST
    user_id = int(request.POST.get('user_id'))
    
    note = Note.objects.create(
        user_id=user_id,
        #directory=0,
        title='untitled',
        started_at=timezone.now(),
        ended_at=timezone.now(),
        created_at=timezone.now(),
        updated_at=timezone.now(),
        content='',
        is_trash=False
    )
    json_res = dict()
    json_res['note_id'] = note.id

    log(request=request, status_code=201, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res, status=201)

def update_note(request):
    coerce_to_post(request)
    request_param = request.PUT

    note_id = int(request.PUT.get('note_id'))
    title = str(request.PUT.get('title'))
    content = str(request.PUT.get('content'))
    started_at = [int(x) for x in str(request.PUT.get('started_at')).split('/')]
    ended_at = [int(x) for x in str(request.PUT.get('ended_at')).split('/')]

    note = Note.objects.get(id=note_id)
    
    note.title = title
    note.content = content
    note.started_at = datetime.datetime(
        started_at[0],
        started_at[1],
        started_at[2],
        started_at[3],
        started_at[4],
        started_at[5],
    )
    note.ended_at = datetime.datetime(
        ended_at[0],
        ended_at[1],
        ended_at[2],
        ended_at[3],
        ended_at[4],
        ended_at[5],
    )
    note.updated_at = timezone.now()
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def delete_note(request):
    coerce_to_post(request)
    request_param = request.DELETE
    note_id = int(request.DELETE.get('note_id'))
    note = Note.objects.get(id=note_id)

    # delete audio files
    audios = Audio.objects.filter(note_id=note_id)
    for audio in audios:
        delete_file_to_s3(settings.AWS_S3_MEDIA_DIR + str(audio.id) + '.webm')
    note.delete()
    
    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def api_note(request):
    try:
        if request.method == 'GET':
            return get_note_info(request)
        elif request.method == 'POST':
            return create_note(request)
        elif request.method == 'PUT':
            return update_note(request)
        elif request.method == 'DELETE':
            return delete_note(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)