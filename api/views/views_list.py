from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.utils import remove_tag
from api.models import User, Note, Directory, Share
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_note_id_shared

@auth_user_id
def get_list_note_all(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    user_email = user.email

    json_res = dict()
    json_res['notes'] = []

    notes = Note.objects.filter(user_id=user_id, is_trash=False).order_by('created_at')
    for note in notes:
        full_content = remove_tag(note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content
        
        color = 0
        if note.directory is None:
            color = -1
        else:
            color = note.directory.color
        
        is_shared = False
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            is_shared = True

        json_res['notes'].append({
            'user_email': user_email,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summary': summary,
            'color': color,
            'is_shared': is_shared
        })
    
    return JsonResponse(json_res)

@auth_user_id
def get_list_note_trash(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    user_email = user.email

    json_res = dict()
    json_res['notes'] = []

    notes = Note.objects.filter(user_id=user_id, is_trash=True).order_by('created_at')
    for note in notes:
        full_content = remove_tag(note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content

        color = 0
        if note.directory is None:
            color = -1
        else:
            color = note.directory.color

        is_shared = False
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            is_shared = True

        json_res['notes'].append({
            'user_email': user_email,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'deleted_at': note.deleted_at,
            'summary': summary,
            'color': color,
            'is_shared': is_shared
        })
    
    return JsonResponse(json_res)

@auth_user_id
def get_list_directory(request):
    user_id = int(request.GET.get('user_id'))

    json_res = dict()
    json_res['directories'] = []

    directories = Directory.objects.filter(user_id=user_id)
    for directory in directories:
        json_res['directories'].append({
            'directory_id': directory.id,
            'name': directory.name
        })
    
    return JsonResponse(json_res)

@auth_directory_id
def get_list_note_by_directory(request):
    directory_id = int(request.GET.get('directory_id'))

    json_res = dict()
    json_res['notes'] = []

    notes = Note.objects.filter(directory_id=directory_id, is_trash=False).order_by('created_at')
    for note in notes:
        full_content = remove_tag(note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content
        
        color = 0
        if note.directory is None:
            color = -1
        else:
            color = note.directory.color

        is_shared = False
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            is_shared = True

        json_res['notes'].append({
            'user_email': note.user.email,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summary': summary,
            'color': color,
            'is_shared': is_shared
        })
    
    return JsonResponse(json_res)

@auth_user_id
def get_list_note_shared(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    user_email = user.email

    json_res = dict()
    json_res['notes'] = []

    shares = Share.objects.filter(user_id=user_id)
    for share in shares:
        if share.note.is_trash == True:
            continue
        full_content = remove_tag(share.note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content

        color = -1
        json_res['notes'].append({
            'user_email': user_email,
            'note_id': share.note.id,
            'title': share.note.title,
            'created_at': share.note.created_at,
            'updated_at': share.note.updated_at,
            'summary': summary,
            'color': color
        })

    return JsonResponse(json_res)

@auth_note_id_shared
def get_list_user_shared(request):
    note_id = int(request.GET.get('note_id'))

    json_res = dict()
    json_res['users'] = []

    shares = Share.objects.filter(note_id=note_id)
    for share in shares:
        json_res['users'].append({
            'user_id': share.user.id,
            'user_name': share.user.name,
            'user_email': share.user.email,
            'user_picture_url': share.user.picture_url
        })
    
    return JsonResponse(json_res)

@log
def api_list_note_all(request):
    try:
        if request.method == 'GET':
            return get_list_note_all(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_list_note_trash(request):
    try:
        if request.method == 'GET':
            return get_list_note_trash(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_list_directory(request):
    try:
        if request.method == 'GET':
            return get_list_directory(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_list_note(request):
    try:
        if request.method == 'GET':
            return get_list_note_by_directory(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_list_note_shared(request):
    try:
        if request.method == 'GET':
            return get_list_note_shared(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_list_user_shared(request):
    try:
        if request.method == 'GET':
            return get_list_user_shared(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)