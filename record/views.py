from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
from pydub import AudioSegment #ffmpeg must be installed in os.

def mylist_html(request):
    return render(request, 'record/mylist.html', {})

def note_html(request):
    return render(request, 'record/note.html', {})

def speech_to_text(filename):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    import io

    input_path = settings.MEDIA_ROOT + '/' + filename + '.flac'

    client = speech.SpeechClient()
    with io.open(input_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='ko-KR',
        enable_word_time_offsets=True)
    response = client.recognize(config, audio)

    return_text = ''
    for result in response.results:
        transcript = result.alternatives[0].transcript
        words = result.alternatives[0].words
        for word_info in words:
            word = word_info.word
            start_secs = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
            end_secs = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
            print(u'Word: {}, Timestamp: {} ~ {} secs'.format(word, start_secs, end_secs))
        return_text = return_text + ' ' + transcript
    print('Result: ' + return_text)
    return return_text

def webm_to_flac(filename):
    input_path = settings.MEDIA_ROOT + '/' + filename + '.webm'
    output_path = settings.MEDIA_ROOT + '/' + filename + '.flac'
    audio = AudioSegment.from_file(input_path, format='webm')
    audio.export(output_path, format='flac')

def audio_stt(request):
    data = request.FILES['data']
    fs = FileSystemStorage()
    fs.save(data.name + '.webm', data)

    webm_to_flac(data.name)
    result = speech_to_text(data.name)

    return HttpResponse(result)
