from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.utils import timezone

from api.utils import coerce_to_post
from api.models import Note
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id

@auth_note_id
def make_trash(request):
    coerce_to_post(request)
    note_id = int(request.PUT.get('note_id'))
    note = Note.objects.get(id=note_id)
    
    note.is_trash = True
    note.deleted_at = timezone.now()
    note.save()

    return HttpResponse(status=200)

@auth_note_id
def cancle_trash(request):
    coerce_to_post(request)
    note_id = int(request.DELETE.get('note_id'))
    note = Note.objects.get(id=note_id)

    note.is_trash = False
    note.save()

    return HttpResponse(status=200)

@auth_directory_id
def delete_directory_note(request):
    coerce_to_post(request)
    directory_id = int(request.PUT.get('directory_id'))
    notes = Note.objects.filter(directory_id=directory_id)
    for note in notes:
        note.is_trash = True
        note.deleted_at = timezone.now()
        note.save()
    
    return HttpResponse(status=200)

@log
def api_note_trash(request):
    try:
        if request.method == 'PUT':
            return make_trash(request)
        elif request.method == 'DELETE':
            return cancle_trash(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_directory_trash(request):
    try:
        if request.method == 'PUT':
            return delete_directory_note(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)