from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Directory
from api.utils import coerce_to_post

def create_directory(request):
    request_param = request.POST
    user_id = int(request.POST.get('user_id'))
    
    directory = Directory.objects.create(
        user_id=user_id,
        name='untitled'
    )
    json_res = dict()
    json_res['directory_id'] = directory.id

    log(request=request, status_code=201, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res, status=201)

def delete_directory(request):
    coerce_to_post(request)
    request_param = request.DELETE
    directory_id = int(request.DELETE.get('directory_id'))
    directory = Directory.objects.get(id=directory_id)

    directory.delete()
    
    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def update_directory(request):
    coerce_to_post(request)
    request_param = request.PUT

    directory_id = int(request.PUT.get('directory_id'))
    name = str(request.PUT.get('name'))

    directory = Directory.objects.get(id=directory_id)
    
    directory.name = name
    directory.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def move_directory(request):
    coerce_to_post(request)
    request_param = request.PUT

    note_id = int(request.PUT.get('note_id'))
    directory_id = int(request.PUT.get('directory_id'))

    note = Note.objects.get(id=note_id)
    note.directory.id = directory_id
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def null_directory(request):
    coerce_to_post(request)
    request_param = request.DELETE

    note_id = int(request.DELETE.get('note_id'))

    note = Note.objects.get(id=note_id)
    note.directory = None
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def api_directory(request):
    try:
        if request.method == 'POST':
            return create_directory(request)
        elif request.method == 'PUT':
            return update_directory(request)
        elif request.method == 'DELETE':
            return delete_directory(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_note_directory(request):
    try:
        if request.method == 'PUT':
            return move_directory(request)
        elif request.method == 'DELETE':
            return null_directory(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)