from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Share
from api.utils import coerce_to_post
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id, auth_sentence_id

@auth_note_id
def make_sharing(request):
    request_param = request.POST
    note_id = int(request.POST.get('note_id'))
    email = str(request.POST.get('email'))
    user = User.objects.get(email=email)
    share = Share.objects.filter(note_id=note_id, user_id=user.id)

    if share.exists():
        return HttpResponse('Already Exist', status=400)
    else:
        Share.objects.create(
        note_id=note_id,
        user_id=user.id
        )
        log(request=request, status_code=201, request_param=request_param)
        return HttpResponse(status=201)

@auth_note_id
def delete_sharing(request):
    coerce_to_post(request)
    request_param = request.DELETE
    note_id = int(request.DELETE.get('note_id'))
    user_id = int(request.DELETE.get('user_id'))
    
    Share.objects.filter(note_id=note_id, user_id=user_id).delete()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def api_note_shared(request):
    try:
        if request.method == 'POST':
            return make_sharing(request)
        elif request.mothod == 'DELETE':
            return delete_sharing(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)