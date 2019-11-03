from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Directory
from api.utils import coerce_to_post
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id

def get_defalut_directory_name(user_id):
    directories = Directory.objects.filter(user_id=user_id)
    directory = directories.filter(name='untitled')
    if not directory.exists():
        return 'untitled'
    else:
        i = 1
        while True:
            name = 'untitled' + str(i)
            directory = directories.filter(name=name)
            if not directory.exists():
                return name
            i = i + 1
            if i > 100:
                return 'untitled'

@auth_user_id
def create_directory(request):
    user_id = int(request.POST.get('user_id'))
    
    directory = Directory.objects.create(
        user_id=user_id,
        name=get_defalut_directory_name(user_id)
    )
    json_res = dict()
    json_res['directory_id'] = directory.id

    return JsonResponse(json_res, status=201)

@auth_directory_id
def delete_directory(request):
    coerce_to_post(request)
    
    directory_id = int(request.DELETE.get('directory_id'))
    directory = Directory.objects.get(id=directory_id)

    directory.delete()
    
    return HttpResponse(status=200)

@auth_directory_id
def update_directory(request):
    coerce_to_post(request)

    directory_id = int(request.PUT.get('directory_id'))
    name = str(request.PUT.get('name'))

    directory = Directory.objects.get(id=directory_id)
    
    directory.name = name
    directory.save()

    return HttpResponse(status=200)

@auth_note_id
@auth_directory_id
def move_to_directory(request):
    coerce_to_post(request)

    note_id = int(request.PUT.get('note_id'))
    directory_id = int(request.PUT.get('directory_id'))

    note = Note.objects.get(id=note_id)
    note.directory_id = directory_id
    note.save()

    return HttpResponse(status=200)

@auth_note_id
def move_to_null_directory(request):
    coerce_to_post(request)

    note_id = int(request.DELETE.get('note_id'))

    note = Note.objects.get(id=note_id)
    note.directory = None
    note.save()

    return HttpResponse(status=200)

@log
def api_directory(request):
    try:
        if request.method == 'POST':
            return create_directory(request)
        elif request.method == 'PUT':
            return update_directory(request)
        elif request.method == 'DELETE':
            return delete_directory(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_note_directory(request):
    try:
        if request.method == 'PUT':
            return move_to_directory(request)
        elif request.method == 'DELETE':
            return move_to_null_directory(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)