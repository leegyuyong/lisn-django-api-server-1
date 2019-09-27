from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.utils import coerce_to_post
from api.models import Note
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_sentence_id

@auth_note_id
def make_trash(request):
    coerce_to_post(request)
    request_param = request.PUT
    note_id = int(request.PUT.get('note_id'))
    note = Note.objects.get(id=note_id)
    
    note.is_trash = True
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

@auth_directory_id
def delete_directory_note(request):
    coerce_to_post(request)
    request_param = request.PUT
    directory_id = int(request.PUT.get('directory_id'))
    note = Note.objects.filter(directory_id=directory_id)

    note.is_trash = True
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def api_note_trash(request):
    try:
        if request.method == 'PUT':
            return make_trash(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_directory_trash(request):
    try:
        if request.method == 'PUT':
            return delete_directory_note(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)