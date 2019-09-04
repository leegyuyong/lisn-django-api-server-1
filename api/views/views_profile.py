from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.models import User
from api.utils import coerce_to_post

def get_profile_info(request):
    request_param = request.GET
    user_id = int(request.GET.get('user_id'))
    user = User.objects.get(id=user_id)
    
    json_res = dict()
    json_res['user_name'] = user.name
    json_res['user_email'] = user.email
    json_res['user_picture_url'] = user.picture_url

    log(request=request, status_code=200, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res)

def api_profile(request):
    try:
        if request.method == 'GET':
            return get_profile_info(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)