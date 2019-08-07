from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

def coerce_to_post(request):
    if request.method == 'PUT' or request.method == 'DELETE':
        method = request.method
        if hasattr(request, '_post'):
            del request._post
            del request._files
        try:
            request.method = 'POST'
            request._load_post_and_files()
            request.method = method
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = method
        if request.method == 'PUT':
            request.PUT = request.POST
        elif request.method == 'DELETE':
            request.DELETE = request.POST