from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.utils import coerce_to_post
from api.models import Note

def make_trash(request):
    coerce_to_post(request)
    request_param = request.PUT
    note_id = int(request.PUT.get('note_id'))
    note = Note.objects.get(id=note_id)
    
    note.is_trash = True
    note.save()

    log(request=request, status_code=200, request_param=request_param)
    return HttpResponse(status=200)

def api_note_trash(request):
    try:
        if request.method == 'PUT':
            return make_trash(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)