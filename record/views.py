from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.conf import settings

def get_mylist_page(request):
    return JsonResponse({
        'url' : '/static/mylist.html'
    })

def manipulate_note(request):
    if request.method == 'GET':
        return JsonResponse({
            'url' : '/static/note.html'
        })
    else:
        return HttpResponse(status=400)

def audio_file_save(request):
    data = request.FILES['data']
    fs = FileSystemStorage()
    fs.save(data.name + '.webm', data)

    return HttpResponse("Audio Saved!")
