from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import boto3
import requests

def upload_file_to_s3(file_object, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file_object, bucket, object_name)
    except:
        return False
    return True

def delete_file_to_s3(bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
    except:
        return False
    return True

def create_presigned_url_s3(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except:
        return ''
    return url
    

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