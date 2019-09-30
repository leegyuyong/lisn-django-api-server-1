from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.utils import coerce_to_post
from api.models import Note
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_sentence_id, auth_note_id_shared

@auth_note_id_shared
def edit_mode(request):
    coerce_to_post(request)
    request_param = request.PUT
    note_id = int(request.PUT.get('note_id'))
    note = Note.objects.get(id=note_id)

    if note.is_edited == True:
        return HttpResponse('Already Editing', status=400)
    else:
        note.is_edited = True
        note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

@auth_note_id_shared
def read_mode(request):
    coerce_to_post(request)
    request_param = request.DELETE
    note_id = int(request.DELETE.get('note_id'))
    note = Note.objects.get(id=note_id)

    note.is_edited = False
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def api_note_edited(request):
    try:
        if request.method == 'PUT':
            return edit_mode(request)
        elif request.method == 'DELETE':
            return read_mode(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)