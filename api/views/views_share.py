from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User, Note, Share
from api.utils import coerce_to_post

def make_sharing(request):
    request_param = request.POST
    note_id = int(request.POST.get('note_id'))
    user_email = str(request.POST.get('user_email'))

    user = User.objects.get(email=user_email)

    share = Share.objects.create(
        note_id=note_id,
        email=user.id
    )
    json_res = dict()
    json_res['share_id'] = share.id

    log(request=request, status_code=201, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res, status=201)

def delete_sharing(request):
    coerce_to_post(request)
    request_param = request.DELETE
    note_id = int(request.DELETE.get('note_id'))
    
    Share.objects.filter(note_id=note_id).delete()

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