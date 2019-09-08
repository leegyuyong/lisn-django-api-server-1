from log import log
import sys
import re

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Directory, Share

def remove_tag(content):
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr, '', content)
   return cleantext

def get_list_note_all(request):
    request_param = request.GET
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    user_name = user.name

    json_res = dict()
    json_res['notes'] = []

    notes = Note.objects.filter(user_id=user_id, is_trash=False).order_by('created_at')
    for note in notes:
        full_content = remove_tag(note.content)
        summery = ''
        if len(full_content) > 20:
            summery = full_content[:20]
        else:
            summery = full_content
        
        json_res['notes'].append({
            'user_name': user_name,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summery': summery
        })
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def get_list_note_trash(request):
    request_param = request.GET
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    user_name = user.name

    json_res = dict()
    json_res['notes'] = []

    notes = Note.objects.filter(user_id=user_id, is_trash=True).order_by('created_at')
    for note in notes:
        json_res['notes'].append({
            'user_name': user_name,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at
        })
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def get_list_directory(request):
    request_param = request.GET
    user_id = int(request.GET.get('user_id'))

    json_res = dict()
    json_res['directories'] = []

    directories = Directory.objects.filter(user_id=user_id)
    for directory in directories:
        json_res['directories'].append({
            'directory_id': directory.id,
            'name': directory.name
        })
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def get_list_note(request):
    request_param = request.GET
    directory_id = int(request.GET.get('directory_id'))

    json_res = dict()
    json_res['notes'] = []

    notes = Note.objects.filter(directory_id=directory_id, is_trash=False).order_by('created_at')
    for note in notes:
        full_content = remove_tag(note.content)
        summery = ''
        if len(full_content) > 20:
            summery = full_content[:20]
        else:
            summery = full_content
        
        json_res['notes'].append({
            #'user_name': user_name,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summery': summery
        })
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def get_list_shared(request):
    request_param = request.GET
    user_id = int(request.GET.get('user_id'))

    json_res = dict()
    json_res['shares'] = []

    shares = Share.objects.filter(email=user_id)

    for share in shares:
        full_content = remove_tag(share.note.content)
        summery = ''
        if len(full_content) > 20:
            summery = full_content[:20]
        else:
            summery = full_content

        json_res['shares'].append({
            'note_id': share.note.id,
            'title': share.note.title,
            'created_at': share.note.created_at,
            'updated_at': share.note.updated_at,
            'summery': summery
        })
        
     
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def get_shared_user(request):
    request_param = request.GET
    note_id = int(request.GET.get('note_id'))

    json_res = dict()
    json_res['shares'] = []

    shares = Share.objects.filter(note_id=note_id)

    for share in shares:
        user = User.objects.get(id=share.email)

        json_res['shares'].append({
            'user_id': share.email,
            'user_email': user.email
        })
    
    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def api_list_note_all(request):
    try:
        if request.method == 'GET':
            return get_list_note_all(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_list_note_trash(request):
    try:
        if request.method == 'GET':
            return get_list_note_trash(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_directory_list(request):
    try:
        if request.method == 'GET':
            return get_list_directory(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_list_note(request):
    try:
        if request.method == 'GET':
            return get_list_note(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_shared_list(request):
    try:
        if request.method == 'GET':
            return get_list_shared(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)

def api_shared_user(request):
    try:
        if request.method == 'GET':
            return get_shared_user(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)