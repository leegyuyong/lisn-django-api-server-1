from log import log
import sys
import datetime
import jwt

from google.oauth2 import id_token
from google.auth.transport import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from api.models import User
from api.utils import coerce_to_post
from config.settings import JWT_SECRET_KEY

CLIENT_ID = '935445294329-t38oc4vmt9l5sokr34h8ueap63dfq4hi.apps.googleusercontent.com'

def get_token(request):
    request_param = request.POST
    token = request.POST.get('google_token')
    user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

    if user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        log(request=request, status_code=400, request_param=request_param)
        return HttpResponse(status=400)

    user_name = user_info['name']
    user_email = user_info['email']
    user_list = User.objects.filter(email=user_email)

    if len(user_list) == 0:
        user = User.objects.create(name=user_name, email=user_email)
    else:
        user = user_list[0]
    
    payload = dict()
    payload['user_id'] = user.id
    payload['email'] = user.email
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*24)
    
    byte_access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    access_token = byte_access_token.decode('utf-8')

    json_res = dict()
    json_res['user_id'] = user.id
    json_res['access_token'] = access_token

    log(request=request, status_code=201, request_param=request_param, json_res=json_res)
    return JsonResponse(json_res, status=201)

def api_token_google(request):
    try:
        if request.method == 'POST':
            return get_token(request)
        else:
            log(request=request, status_code=405)
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(request=request, status_code=400)
        return HttpResponse(status=400)