from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.utils import coerce_to_post
from api.models import Note
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_note_id_shared, auth_note_id_edit

@auth_note_id_shared
@auth_note_id_edit
def edit_mode(request):
    coerce_to_post(request)
    user_id = int(request.PUT.get('user_id'))
    note_id = int(request.PUT.get('note_id'))
    note = Note.objects.get(id=note_id)
    
    note.edit_user = user_id
    note.save()

    return HttpResponse(status=200)

@auth_note_id_shared
def read_mode(request):
    coerce_to_post(request)
    user_id = int(request.DELETE.get('user_id'))
    note_id = int(request.DELETE.get('note_id'))
    note = Note.objects.get(id=note_id)

    if note.edit_user == user_id:
        note.edit_user = None
        note.save()
    else:
        return HttpResponse('Only editing user can change mode', status=400)

    return HttpResponse(status=200)

@log
def api_note_edited(request):
    try:
        if request.method == 'PUT':
            return edit_mode(request)
        elif request.method == 'DELETE':
            return read_mode(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)