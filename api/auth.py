import sys
import copy
import jwt

from django.http import HttpResponse, JsonResponse, QueryDict

from config.settings import JWT_SECRET_KEY
from api.models import User, Note, Directory, Audio, Sentence, Share
from api.utils import coerce_to_post

AUTH = True

def extract_id(request, target):
    if request.method == 'GET':
        return int(request.GET.get(target))
    elif request.method == 'POST':
        return int(request.POST.get(target))
    elif request.method == 'PUT':
        coerce_to_post(request)
        return int(request.PUT.get(target))
    elif request.method == 'DELETE':
        coerce_to_post(request)
        return int(request.DELETE.get(target))
    else:
        return -1

def extract_user_id_from_jwt(request):
    auth = request.META['HTTP_AUTHORIZATION']
    access_token = auth.split()[1]
    byte_access_token = access_token.encode('utf-8')
    payload = jwt.decode(byte_access_token, JWT_SECRET_KEY, algorithm='HS256')
    return int(payload['user_id'])

def is_valid_user_id(request, user_id):
    User.objects.get(id=user_id)

    if extract_user_id_from_jwt(request) == user_id:
        return True
    else:
        return False

def is_valid_note_id(request, note_id):
    note = Note.objects.get(id=note_id)
    user_id = note.user.id
    return is_valid_user_id(request, user_id)

def is_valid_directory_id(request, directory_id):
    directory = Directory.objects.get(id=directory_id)
    user_id = directory.user.id
    return is_valid_user_id(request, user_id)

def is_valid_audio_id(request, audio_id):
    audio = Audio.objects.get(id=audio_id)
    user_id = audio.user.id
    return is_valid_user_id(request, user_id)

def is_valid_sentence_id(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    user_id = sentence.user.id
    return is_valid_user_id(request, user_id)

def is_valid_note_id_shared(request, note_id):
    if is_valid_note_id(request, note_id):
        return True

    # Check if this person is shared
    user_id_jwt = extract_user_id_from_jwt(request)

    share = Share.objects.filter(note_id=note_id, user_id=user_id_jwt)
    if share.exists():
        return True
    else:
        return False

def is_valid_note_id_edited(request, note_id):
    # Check ohter user already edited
    note = Note.objects.get(id=note_id)
    user_id_jwt = extract_user_id_from_jwt(request)
    
    if note.edit_user == user_id_jwt:
        return True
    elif note.edit_user == None:
        return True
    else:
        return False

def is_valid_sentence_id_shared(request, sentence_id):
    if is_valid_sentence_id(request, sentence_id):
        return True

    # Check if this person is shared
    sentence = Sentence.objects.get(id=sentence_id)
    note_id = sentence.audio.note.id
    user_id_jwt = extract_user_id_from_jwt(request)

    share = Share.objects.filter(note_id=note_id, user_id=user_id_jwt)
    if share.exists():
        return True
    else:
        return False

def is_valid_sentence_id_edited(request, sentence_id):
    # Check ohter user already edited
    sentence = Sentence.objects.get(id=sentence_id)
    note_id = sentence.audio.note.id
    note = Note.objects.get(id=note_id)
    user_id_jwt = extract_user_id_from_jwt(request)

    if note.edit_user == user_id_jwt:
        return True
    else:
        return False

def is_valid_audio_id_shared(request, audio_id):
    if is_valid_audio_id(request, audio_id):
        return True
    
    # Check if this person is shared
    audio = Audio.objects.get(id=audio_id)
    note_id = audio.note.id
    user_id_jwt = extract_user_id_from_jwt(request)

    share = Share.objects.filter(note_id=note_id, user_id=user_id_jwt)
    if share.exists():
        return True
    else:
        return False
    
def auth_user_id(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            user_id = extract_id(request, 'user_id')
            if user_id == -1:
                return HttpResponse(status=405)

            if is_valid_user_id(request, user_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_note_id(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            note_id = extract_id(request, 'note_id')
            if note_id == -1:
                return HttpResponse(status=405)

            if is_valid_note_id(request, note_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_directory_id(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            directory_id = extract_id(request, 'directory_id')
            if directory_id == -1:
                return HttpResponse(status=405)

            if is_valid_directory_id(request, directory_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_audio_id(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            audio_id = extract_id(request, 'audio_id')
            if audio_id == -1:
                return HttpResponse(status=405)

            if is_valid_audio_id(request, audio_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_note_id_shared(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            note_id = extract_id(request, 'note_id')
            if note_id == -1:
                return HttpResponse(status=405)

            if is_valid_note_id_shared(request, note_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_note_id_edit(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            note_id = extract_id(request, 'note_id')
            if note_id == -1:
                return HttpResponse(status=405)

            if is_valid_note_id_edited(request, note_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_sentence_id_shared(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            sentence_id = extract_id(request, 'sentence_id')
            if sentence_id == -1:
                return HttpResponse(status=405)

            if is_valid_sentence_id_shared(request, sentence_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_sentence_id_edit(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            sentence_id = extract_id(request, 'sentence_id')
            if sentence_id == -1:
                return HttpResponse(status=405)

            if is_valid_sentence_id_edited(request, sentence_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api

def auth_audio_id_shared(api):
    if AUTH == False:
        return api

    def valid_api(*args, **kwargs):
        request = args[0]
        try:
            audio_id = extract_id(request, 'audio_id')
            if audio_id == -1:
                return HttpResponse(status=405)

            if is_valid_audio_id_shared(request, audio_id) == True:
                return api(request)
            else:
                return HttpResponse(status=401)
        except jwt.ExpiredSignatureError:
            return HttpResponse(status=401)
        except:
            return HttpResponse(status=400)
    return valid_api