from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import User

import os
import sys
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt

CLIENT_ID = '935445294329-5mpgtul9b7ibvc56co139f2ullou1p6f.apps.googleusercontent.com'

def oauth_google(request):
    #try:
        token = request.POST['idtoken']
        user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return HttpResponse(status=403)

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
        
        json_res = dict()
        json_res['redirect_url'] = '/mylist.html'
        json_res['user_id'] = user.id

        return JsonResponse(json_res)
    #except:
        #print("Unexpected error:", sys.exc_info()[0])
        #return HttpResponse(status=400)