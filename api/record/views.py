import os
import sys
import re

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from api.user.models import User
from api.user.util import auth_validate_check
from api.record.models import Note, Audio, Sentence
from api.record.util import coerce_to_post, upload_file_to_s3, delete_file_to_s3, create_presigned_url_s3
from config.settings import JWT_SECRET_KEY
import log

def remove_tag(content):
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr, '', content)
   return cleantext

def get_list(request):
    try:
        if request.method == 'GET':
            request_param = request.GET
            user_id = int(request.GET.get('user_id'))
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)

            json_res = dict()
            json_res['user_id'] = user_id
            json_res['notes'] = []

            notes = Note.objects.filter(user_id=user_id, is_trash=False).order_by('created_at')
            for note in notes:
                full_content = remove_tag(note.content)
                summery = ''
                if len(full_content) > 20:
                    summery = full_content[:20]
                else:
                    summery = full_content
                json_res['notes'].append({
                    'note_id': note.id,
                    'title': note.title,
                    'created_at': note.created_at,
                    'updated_at': note.updated_at,
                    'summery': summery
                })
            
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=200\n')
            return JsonResponse(json_res)
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)

def manipulate_note(request):
    try:
        if request.method == 'GET':
            request_param = request.GET
            note_id = int(request.GET.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id

            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)

            json_res = dict()
            json_res['note_id'] = note.id
            json_res['title'] = note.title
            json_res['content'] = note.content
            json_res['audios'] = []

            audios = Audio.objects.filter(note_id=note_id).order_by('id')
            for audio in audios:
                json_audio = dict()
                json_audio['audio_id'] = audio.id
                json_audio['sentences'] = []

                sentences = Sentence.objects.filter(audio_id=audio.id).order_by('index')
                for sentence in sentences:
                    json_sentence = dict()
                    json_sentence['sentence_id'] = sentence.id
                    json_sentence['started_at'] = sentence.started_at
                    json_sentence['ended_at'] = sentence.ended_at
                    json_sentence['content'] = sentence.content
                    json_audio['sentences'].append(json_sentence)

                json_res['audios'].append(json_audio)
            
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=200\n')
            return JsonResponse(json_res)
        elif request.method == 'POST':
            request_param = request.POST
            user_id = int(request.POST.get('user_id'))
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            note = Note.objects.create(
                user_id=user_id,
                title='untitled',
                created_at=timezone.now(),
                updated_at=timezone.now(),
                content='',
                is_trash=False
            )
            json_res = dict()
            json_res['note_id'] = note.id

            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=201\n')
            return JsonResponse(json_res, status=201)
        elif request.method == 'PUT':
            coerce_to_post(request)
            request_param = request.PUT
            title = str(request.PUT.get('title'))
            content = str(request.PUT.get('content'))
            note_id = int(request.PUT.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            note.title = title
            note.content = content
            note.updated_at = timezone.now()
            note.save()

            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=200\n')
            return HttpResponse(status=200)
        elif request.method == 'DELETE':
            coerce_to_post(request)
            request_param = request.DELETE
            note_id = int(request.DELETE.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            # delete audio files
            audios = Audio.objects.filter(note_id=note_id)
            for audio in audios:
                delete_file_to_s3('audio/' + str(audio.id) + '.webm')
            note.delete()
            
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=200\n')
            return HttpResponse(status=200)
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)

def throw_away_note(request):
    try:
        if request.method == 'PUT':
            coerce_to_post(request)
            request_param = request.PUT
            note_id = int(request.PUT.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            note.is_trash = True
            note.save()

            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=200\n')
            return HttpResponse(status=200)
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)

def get_trash_list(request):
    try:
        if request.method == 'GET':
            request_param = request.GET
            user_id = int(request.GET.get('user_id'))
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)

            json_res = dict()
            json_res['user_id'] = user_id
            json_res['notes'] = []

            notes = Note.objects.filter(user_id=user_id, is_trash=True).order_by('created_at')
            for note in notes:
                json_res['notes'].append({
                    'note_id': note.id,
                    'title': note.title,
                    'created_at': note.created_at,
                    'updated_at': note.updated_at
                })
            
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=200\n')
            return JsonResponse(json_res)
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)

def manipulate_audio(request):
    try:
        if request.method == 'GET':
            request_param = request.GET
            audio_id = int(request.GET.get('audio_id'))
            audio = Audio.objects.get(id=audio_id)
            user_id = audio.user.id
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            json_res = dict()
            json_res['data_url'] = create_presigned_url_s3('audio/' + str(audio.id) + '.webm')

            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=200\n')
            return JsonResponse(json_res)
        elif request.method == 'POST':
            request_param = request.POST
            note_id = int(request.POST.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            note.updated_at = timezone.now()
            note.save()
            
            audio = Audio.objects.create(
                note_id=note_id,
                user_id=user_id
            )

            audio_data = request.FILES['audio_data']
            upload_file_to_s3(audio_data, 'audio/' + str(audio.id) + '.webm')
            
            json_res = dict()
            json_res['audio_id'] = audio.id
            
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=201\n')
            return JsonResponse(json_res, status=201)
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)

def manipulate_sentence(request):
    try:
        if request.method == 'POST':
            request_param = request.POST
            index = int(request.POST.get('index'))
            audio_id = int(request.POST.get('audio_id'))
            started_at = int(request.POST.get('started_at'))
            ended_at = int(request.POST.get('ended_at'))
            content = str(request.POST.get('content'))
            audio = Audio.objects.get(id=audio_id)
            user_id = audio.user.id
            
            if auth_validate_check(request, user_id) == False:
                log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=401\n')
                return HttpResponse(status=401)
            
            sentence = Sentence.objects.create(
                index=index,
                audio_id=audio_id,
                user_id=user_id,
                started_at=started_at,
                ended_at=ended_at,
                content=content
            )
            json_res = dict()
            json_res['sentence_id'] = sentence.id
            
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=201\n')
            return JsonResponse(json_res, status=201)
        else:
            log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=405\n')
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log.logger.debug(str(request) + '\n' + str(request_param) + '\n' + 'status=400\n')
        return HttpResponse(status=400)