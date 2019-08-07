from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import User

import os
import sys
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests

import jwt
from GoodListener.settings import JWT_SECRET_KEY

CLIENT_ID = '935445294329-5mpgtul9b7ibvc56co139f2ullou1p6f.apps.googleusercontent.com'

def auth_validate_check(request, user_id):
    try:
        auth_token = request.session['auth_token']
        byte_auth_token = auth_token.encode('utf-8')
        payload = jwt.decode(byte_auth_token, JWT_SECRET_KEY, algorithm='HS256')
        if payload['user_id'] == user_id:
            user = User.objects.get(id=user_id)
            if user.token == auth_token:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def signin(request):
    try:
        if request.method == 'POST':
            token = request.POST.get('idtoken')
            user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            if user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return HttpResponse(status=400)

            user_name = user_info['name']
            user_email = user_info['email']
            user_list = User.objects.filter(email=user_email)

            if len(user_list) == 0:
                user = User.objects.create(name=user_name, email=user_email, token='_')
            else:
                user = user_list[0]
            
            payload = dict()
            payload['user_id'] = user.id
            payload['email'] = user.email
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*24)
            
            byte_auth_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
            auth_token = byte_auth_token.decode('utf-8')
            user.token = auth_token
            user.save()

            request.session['auth_token'] = auth_token

            json_res = dict()
            json_res['redirect_url'] = '/mylist.html'
            json_res['user_id'] = user.id

            return JsonResponse(json_res, status=201)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

def delete_token(request):
    try:
        if request.method == 'DELETE':
            request.session.flush()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)