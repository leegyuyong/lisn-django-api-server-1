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

def webm_to_wav(filename):
    from pydub import AudioSegment #ffmpeg must be installed in os.
    input_path = settings.MEDIA_ROOT + '/' + filename + '.webm'
    output_path = settings.MEDIA_ROOT + '/' + filename + '.wav'
    audio = AudioSegment.from_file(input_path, format='webm')
    audio.export(output_path, format='wav')

def audio_file_save(request):
    data = request.FILES['data']
    fs = FileSystemStorage()
    fs.save(data.name + '.webm', data)

    #webm_to_wav(data.name)

    return HttpResponse("Audio Saved!")
