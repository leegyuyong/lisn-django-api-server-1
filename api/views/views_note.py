from log import log
import sys
import datetime

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.utils import timezone

from api.models import Note, Audio, Sentence
from api.utils import coerce_to_post
from api.s3_client.s3_client import delete_file_to_s3
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_note_id_shared, auth_note_id_edit
from api.es_client.es_client import es

def get_defalut_note_title(user_id):
    notes = Note.objects.filter(user_id=user_id)
    note = notes.filter(title='untitled')
    if not note.exists():
        return 'untitled'
    else:
        i = 1
        while True:
            title = 'untitled' + str(i)
            note = notes.filter(title=title)
            if not note.exists():
                return title
            i = i + 1
            if i > 100:
                return 'untitled'

@auth_note_id_shared
def get_note_info(request):
    note_id = int(request.GET.get('note_id'))
    note = Note.objects.get(id=note_id)

    json_res = dict()
    json_res['note_id'] = note.id
    json_res['title'] = note.title
    json_res['content'] = note.content
    json_res['created_at'] = note.created_at
    json_res['updated_at'] = note.updated_at

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
    
    return JsonResponse(json_res)

@auth_user_id
def create_note(request):
    user_id = int(request.POST.get('user_id'))
    
    note = Note.objects.create(
        user_id=user_id,
        title=get_defalut_note_title(user_id),
        created_at=timezone.now(),
        updated_at=timezone.now(),
        deleted_at=timezone.now(),
        content='',
        is_trash=False
    )
    json_res = dict()
    json_res['note_id'] = note.id

    # elasticsearch document create
    es_document = dict()
    es_document['note_id'] = note.id
    es_document['user_id'] = note.user.id
    es_document['title'] = note.title
    es_document['content'] = note.content
    es.create(index='note', body=es_document, id=note.id)

    return JsonResponse(json_res, status=201)

@auth_note_id_shared
@auth_note_id_edit
def update_note(request):
    coerce_to_post(request)

    note_id = int(request.PUT.get('note_id'))
    title = str(request.PUT.get('title'))
    content = str(request.PUT.get('content'))

    note = Note.objects.get(id=note_id)
    
    note.title = title
    note.content = content
    note.updated_at = timezone.now()
    note.save()

    # elasticsearch document update
    es_document = dict()
    es_document['title'] = note.title
    es_document['content'] = note.content
    es.update(index='note', body={'doc':es_document}, id=note.id)

    return HttpResponse(status=200)

@auth_note_id
def delete_note(request):
    coerce_to_post(request)
    note_id = int(request.DELETE.get('note_id'))
    note = Note.objects.get(id=note_id)

    # delete audio files
    audios = Audio.objects.filter(note_id=note_id)
    for audio in audios:
        delete_file_to_s3(settings.AWS_S3_MEDIA_DIR + str(audio.id) + '.webm')
        # elasticsearch document delete
        sentences = Sentence.objects.filter(audio_id=audio.id)
        for sentence in sentences:
            es.delete(index='sentence', id=sentence.id)
    
    # elasticsearch document delete
    es.delete(index='note', id=note.id)

    note.delete()

    return HttpResponse(status=200)

@log
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
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)