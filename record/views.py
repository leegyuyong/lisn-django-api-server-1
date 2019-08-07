import os
import sys

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from signin.models import User
from .models import Note, Audio, Sentence
from pydub import AudioSegment #ffmpeg must be installed in os.
from .util import coerce_to_post
from signin.views import auth_validate_check

def webm_to_wav(filename):
    input_path = settings.MEDIA_ROOT + '/' + filename + '.webm'
    output_path = settings.MEDIA_ROOT + '/' + filename + '.wav'
    audio = AudioSegment.from_file(input_path, format='webm')
    audio.export(output_path, format='wav')

def get_list(request):
    try:
        if request.method == 'GET':

            user_id = int(request.GET.get('user_id'))
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)

            json_res = dict()
            json_res['user_id'] = user_id
            json_res['notes'] = []

            notes = Note.objects.filter(user_id=user_id).order_by('created_at')
            for note in notes:
                json_res['notes'].append({
                    'note_id': note.id,
                    'title': note.title,
                    'created_at': note.created_at,
                    'updated_at': note.updated_at
                })
            
            return JsonResponse(json_res)
        else:
            return HttpResponse(status=400)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

def delete_audio_files(note_id):
    audios = Audio.objects.filter(note_id=note_id)
    for audio in audios:
        sentences = Sentence.objects.filter(audio_id=audio.id)
        for sentence in sentences:
            if os.path.exists(sentence.data_url):
                os.remove(sentence.data_url)
        if os.path.exists(audio.data_url):
            os.remove(audio.data_url)

def manipulate_note(request):
    try:
        if request.method == 'GET':
            note_id = int(request.GET.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id

            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)

            json_res = dict()
            json_res['title'] = note.title
            json_res['content'] = note.content
            json_res['audios'] = []

            audios = Audio.objects.filter(note_id=note_id).order_by('id')
            for audio in audios:
                json_audio = dict()
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
            
            return JsonResponse(json_res)
        elif request.method == 'POST':
            user_id = int(request.POST.get('user_id'))
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)
            
            note = Note.objects.create(
                user_id=user_id,
                title='untitled',
                created_at=timezone.now(),
                updated_at=timezone.now(),
                content=''
            )
            json_res = dict()
            json_res['note_id'] = note.id

            return JsonResponse(json_res, status=201)
        elif request.method == 'PUT':
            coerce_to_post(request)
            title = str(request.PUT.get('title'))
            content = str(request.PUT.get('content'))
            note_id = int(request.PUT.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)
            
            note.title = title
            note.content = content
            note.updated_at = timezone.now()
            note.save()

            return HttpResponse(status=200)
        elif request.method == 'DELETE':
            coerce_to_post(request)
            note_id = int(request.DELETE.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)
            
            delete_audio_files(note_id)
            note.delete()
            
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

def save_audio(request):
    try:
        if request.method == 'POST':
            note_id = int(request.POST.get('note_id'))
            note = Note.objects.get(id=note_id)
            user_id = note.user.id
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)
            
            note.updated_at = timezone.now()
            note.save()

            audio = Audio.objects.create(
                note_id=note_id,
                user_id=user_id,
                data_url=''
            )

            audio_id = audio.id
            filename = str(user_id) + '_' + str(note_id) + '_' + str(audio_id)
            audio_data = request.FILES['audio_data']
            fs = FileSystemStorage()
            fs.save(filename + '.webm', audio_data)
            #webm_to_wav(filename)
            
            audio.data_url = settings.MEDIA_ROOT + '/' + filename + '.webm'
            audio.save()

            json_res = dict()
            json_res['audio_id'] = audio_id
            
            return JsonResponse(json_res, status=201)
        else:
            return HttpResponse(status=400)    
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

def split_audio(data_url, index, started_at, ended_at):
    audio = AudioSegment.from_file(data_url, format='webm')
    if ended_at == -1:
        ended_at = len(audio)
    elif ended_at > len(audio):
        return False, '/'
    audio_seg = audio[started_at:ended_at]

    ex_extension = data_url.split('.')[0]
    new_data_url = ex_extension + '_' + str(index) + '.webm'
    audio_seg.export(new_data_url, format='webm')
    return True, new_data_url

def manipulate_sentence(request):
    try:
        if request.method == 'GET':
            sentence_id = int(request.GET.get('sentence_id'))
            sentence = Sentence.objects.get(id=sentence_id)
            user_id = sentence.user.id
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)
            
            data_url = sentence.data_url
            try:
                fs = open(data_url, "rb")
                response = HttpResponse(status=200)
                response.write(fs.read())
            except:
                return HttpResponse(status=400)
            response['Content-Type'] ='audio/webm'
            response['Content-Length'] = os.path.getsize(data_url)

            return response
        elif request.method == 'POST':
            index = int(request.POST.get('index'))
            audio_id = int(request.POST.get('audio_id'))
            started_at = int(request.POST.get('started_at'))
            ended_at = int(request.POST.get('ended_at'))
            content = str(request.POST.get('content'))
            audio = Audio.objects.get(id=audio_id)
            user_id = audio.user.id
            
            if auth_validate_check(request, user_id) == False:
                return HttpResponse(status=403)
            
            is_ok, data_url = split_audio(audio.data_url, index, started_at, ended_at)
            if is_ok == True:
                sentence = Sentence.objects.create(
                    index=index,
                    audio_id=audio_id,
                    user_id=user_id,
                    started_at=started_at,
                    ended_at=ended_at,
                    content=content,
                    data_url=data_url
                )
                json_res = dict()
                json_res['sentence_id'] = sentence.id
                
                return JsonResponse(json_res, status=201)
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)