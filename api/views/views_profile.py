from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User
from api.utils import coerce_to_post
from api.auth import auth_user_id, auth_directory_id, auth_note_id, auth_audio_id

@auth_user_id
def get_profile_info(request):
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    
    json_res = dict()
    json_res['user_name'] = user.name
    json_res['user_email'] = user.email
    json_res['user_picture_url'] = user.picture_url
    
    return JsonResponse(json_res)

@log
def api_profile(request):
    try:
        if request.method == 'GET':
            return get_profile_info(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)