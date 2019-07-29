from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def get_signin_page(request):
    return JsonResponse({
        'url' : '/static/signin.html'
    })