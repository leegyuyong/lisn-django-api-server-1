var recordButton = document.getElementById('record_btn');
var sentence_list = document.getElementById('audio_stt_result_list');
var state_text = document.getElementById('state_text');

var setCookie = function(name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp*24*60*60*1000);
    document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
};
var getCookie = function(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
};

var is_record = false;
var recorder;
var chunks;
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'ko-KR';
recognition.maxAlternatives = 1;

var audio_start_time;
var audio_timestamp = [];
var tmp_id;
var is_first_word;
var continuous;

var render_stt_text = function(e, id) {
    var sentence_tag = document.getElementById(id);
    var transcript = '';
    for (var i = e.resultIndex; i < e.results.length; ++i) {
        transcript += e.results[i][0].transcript;
    }
    sentence_tag.textContent = transcript;
    sentence_tag.style.color = '#666666';
};

var startRecording = function(stream) {

    recorder = new MediaRecorder(stream);
    chunks = [];

    recognition.onstart = function() {
       is_first_word = true;
       tmp_id = 0;
       continuous = true;
    };

    recognition.onend = function() {
        if(continuous == true) {
            recognition.start();
            //console.log('Recognition restart!');
        }
    }

    recognition.onresult = function(e) {
        var last = e.results.length - 1;
        var transcript = e.results[last][0].transcript;
        if(transcript == null) {
            return;
        }

        if(e.results[last].isFinal == true) {
            var sentence_tag = document.getElementById('tmp_' + tmp_id);
            sentence_tag.textContent = transcript;
            sentence_tag.style.color = '#000000';
            is_first_word = true;
            tmp_id++;
        }
        else {
            if(is_first_word == true) {
                var word_start_time = Date.now() - audio_start_time;
                if(word_start_time - 2300 > 0){
                    word_start_time -= 2300;
                }
                else{
                    word_start_time = 0;
                }
                audio_timestamp.push(word_start_time);
                //console.log(word_start_time);

                is_first_word = false;
                var sentence_tag = document.createElement('h4');
                var newline = document.createElement('hr');
                sentence_tag.id = 'tmp_' + tmp_id;
                sentence_tag.className = "audio_stt_result";
                sentence_list.appendChild(sentence_tag);
                sentence_list.appendChild(newline);
                render_stt_text(e, 'tmp_' + tmp_id);
            }
            else {
                render_stt_text(e, 'tmp_' + tmp_id);
            }
        }
        //console.log(e.results);
    };

    recorder.onstart = function() {
        audio_start_time = Date.now();
    };

    recorder.ondataavailable = function(e) {
        chunks.push(e.data);
    };

    recorder.onstop = function(e) {
        sendRecording();
    };

    recorder.start();
    recognition.start();
};

var get_audio_and_play = function(sentence_id) {
    window.AudioContext = window.AudioContext||window.webkitAudioContext||window.mozAudioContext;
    var audio_context = new AudioContext();
    var source = audio_context.createBufferSource();
    var uri = '/record/sentence' + '?' + 'sentence_id=' + sentence_id;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', uri);
    xhr.responseType = 'arraybuffer';
    xhr.send();
    xhr.onload = function() {
        audio_context.decodeAudioData(xhr.response, function(buffer) {
            source.buffer = buffer;
            source.connect(audio_context.destination);
            source.start(0);
        }, null);
    };
};

var post_record_sentence = function(formData, tmp_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/record/sentence');
    xhr.send(formData);
    xhr.onload = function() {
        var sentence_id = JSON.parse(xhr.responseText)['sentence_id'];
        var sentence_tag = document.getElementById(tmp_id);
        sentence_tag.id = sentence_id;
        sentence_tag.onclick = function(event) {
            get_audio_and_play(event.target.id);
        };
    };
};

var sendRecording = function() {
    var blob = new Blob(chunks, {'type': 'audio/webm;'});
    // clear chunks
    chunks = [];

    if(audio_timestamp.length == 0){
        return;
    }

    var note_id = getCookie('glisn_note_id');
    var formData = new FormData();
    formData.append('audio_data', blob, 'filename');
    formData.append('note_id', note_id);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/record/audio');
    xhr.send(formData);
    xhr.onload = function() {
        var audio_id = JSON.parse(xhr.responseText)['audio_id'];
        audio_timestamp.push(-1);
        for(var i=1; i<audio_timestamp.length; i++){
            if(audio_timestamp[i] == audio_timestamp[i-1]){
                audio_timestamp[i] = audio_timestamp[i-1]+1;
            }
            var started_at = audio_timestamp[i-1];
            var ended_at = audio_timestamp[i];
            var sentence_tag = document.getElementById('tmp_' + (i-1));
            var content = sentence_tag.textContent;
            
            var formData = new FormData();
            formData.append('index', (i-1));
            formData.append('audio_id', audio_id);
            formData.append('started_at', started_at);
            formData.append('ended_at', ended_at);
            formData.append('content', content);
            post_record_sentence(formData, 'tmp_' + (i-1));
        }

        audio_timestamp = [];
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