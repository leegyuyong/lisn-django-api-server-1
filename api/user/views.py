import os
import sys
import datetime
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from api.user.models import User
from api.user.util import auth_validate_check
from api.record.util import coerce_to_post
from config.settings import JWT_SECRET_KEY
import log

CLIENT_ID = '935445294329-t38oc4vmt9l5sokr34h8ueap63dfq4hi.apps.googleusercontent.com'

def signin(request):
    try:
        if request.method == 'POST':
            request_param = request.POST
            token = request.POST.get('idtoken')
            user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            if user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
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
            json_res['redirect_url'] = '/mylist.html'
            json_res['user_id'] = user.id

            response = JsonResponse(json_res, status=201)
            response.set_cookie('access_token', access_token, httponly=True)

            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=201\n')
            return response
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)

def delete_token(request):
    try:
        if request.method == 'DELETE':
            coerce_to_post(request)
            request_param = request.DELETE
            response = HttpResponse(status=200)
            response.delete_cookie('access_token')
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=200\n')
            return response
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)