var recordButton = document.getElementById('record_btn');
var audio_stt_result_list = document.getElementById('audio_stt_result_list');
var state_text = document.getElementById('state_text');

var is_record = false;
var recorder;
var chunks;
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'ko-KR';
recognition.maxAlternatives = 1;

var audio_start_time;
var word_idx = 0;
var is_first_word;
var prev;
var continuous;

var startRecording = function(stream) {

    recorder = new MediaRecorder(stream);
    chunks = [];

    recognition.onstart = function() {
       is_first_word = true;
       prev = -1;
       continuous = true;
    };

    recognition.onend = function() {
        if(continuous == true) {
            recognition.start();
            console.log('Recognition restart!');
        }
    }

    recognition.onresult = function(e) {
        var last = e.results.length - 1;
        var transcript = e.results[last][0].transcript;
        if(transcript == null) {
            return;
        }

        if(e.results[last].isFinal == true) {
            var audio_stt_result = document.getElementById('w' + word_idx);
            audio_stt_result.textContent = transcript;
            audio_stt_result.style.color = '#000000';
            is_first_word = true;
            word_idx++;
            prev = last;
        }
        else {
            if(is_first_word == true) {
                var word_start_time = Date.now() - audio_start_time;
                console.log(word_start_time);
                is_first_word = false;

                var audio_stt_result = document.createElement('h3');
                audio_stt_result.id = 'w' + word_idx;
                audio_stt_result.className = "audio_stt_result";
                audio_stt_result.textContent = transcript;
                audio_stt_result.style.color = '#666666';
                audio_stt_result.style.backgroundColor = '#FFFFCC';
                audio_stt_result_list.appendChild(audio_stt_result);
            }
            else {
                var audio_stt_result = document.getElementById('w' + word_idx);
                var text_tmp = '';
                for(var i = prev + 1; i < last; i++) {
                    text_tmp += e.results[i][0].transcript;
                }
                if(audio_stt_result.textContent != text_tmp)
                    audio_stt_result.textContent = text_tmp;
            }
        }
        //console.log(e.results);
    };

    recorder.ondataavailable = function(e) {
        chunks.push(e.data);
    };

    recorder.onstop = function(e) {
        sendRecording();
    };

    audio_start_time = Date.now();
    recorder.start();
    recognition.start();
};

var sendRecording = function() {
    var blob = new Blob(chunks, {'type': 'audio/webm;'});
    var fileName = Date.now();

    // clear chunks
    chunks = [];

    var formData = new FormData();
    formData.append('data', blob, fileName);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/record/audio');
    xhr.send(formData);
    xhr.onload = function() {
        console.log(xhr.responseText);
    };
};

recordButton.onclick = function() {
    if(is_record == false) {
        console.log('Start');
        state_text.textContent = "Recording...";

        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(startRecording);
        recordButton.textContent = "STOP";
        recordButton.className = "btn btn-danger";
        is_record = true;
    }
    else {
        console.log('Stop');
        state_text.textContent = "";

        continuous = false;
        recognition.stop();
        recorder.stop();
        recordButton.textContent = "RECORD";
        recordButton.className = "btn btn-success";
        is_record = false;
    }
};