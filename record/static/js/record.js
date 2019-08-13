var recordButton = document.getElementById('record_btn');
var pauseButton = document.getElementById('pause_btn');
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

var audio = new Audio();
var is_record = false;
var recorder;
var chunks;

var audio_start_time;
var audio_timestamp = [];
var tmp_id = 0;
var current_start_tmp_id;
var is_first_word;

var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'ko-KR';
recognition.maxAlternatives = 1;

var update_sentence_text = function(tmp_sentence_id, event_object_list) {
    var sentence_tag = document.getElementById(tmp_sentence_id);
    var transcript = '';
    for (var i = event_object_list.resultIndex; i < event_object_list.results.length; ++i) {
        transcript += event_object_list.results[i][0].transcript;
    }
    sentence_tag.textContent = transcript;
    sentence_tag.style.color = '#666666';
};

var startRecording = function(stream) {

    recorder = new MediaRecorder(stream);
    chunks = [];
    is_first_word = true;
    current_start_tmp_id = tmp_id;

    // recorder setting
    recorder.onstart = function() {
        audio_start_time = Date.now();
    };

    recorder.ondataavailable = function(e) {
        chunks.push(e.data);
    };

    recorder.onstop = function(e) {
        sendRecording();
    };

    recognition.onend = function() {
        if(is_record == true) {
            recognition.start();
            console.log('Recognition restart!');
        }
    }

    // recognition setting
    recognition.onresult = function(event_object_list) {
        var event_last_idx = event_object_list.results.length - 1;
        var transcript = event_object_list.results[event_last_idx][0].transcript;
        if(transcript == null) {
            return;
        }

        if(event_object_list.results[event_last_idx].isFinal == true) {
            var sentence_tag = document.getElementById('tmp_' + tmp_id);
            sentence_tag.textContent = transcript;
            sentence_tag.style.color = '#000000';
            is_first_word = true;
            tmp_id++;
        }
        else if(is_first_word == true) {
            var word_start_time = Date.now() - audio_start_time;
            if(word_start_time - 2300 > 0){
                word_start_time -= 2300;
            }
            else{
                word_start_time = 0;
            }
            audio_timestamp.push(word_start_time);
            
            // make new sentence tag
            var sentence_tag = document.createElement('h4');
            var newline = document.createElement('hr');
            sentence_tag.id = 'tmp_' + tmp_id;
            sentence_tag.className = "audio_stt_result";
            sentence_list.appendChild(sentence_tag);
            sentence_list.appendChild(newline);
            update_sentence_text('tmp_' + tmp_id, event_object_list);
            is_first_word = false;
        }
        else {
            update_sentence_text('tmp_' + tmp_id, event_object_list);
        }
        //console.log(event_object_list.results);
    };

    // start recorder and recognition
    recorder.start();
    recognition.start();
};

var get_audio_and_play = function(sentence_id, index, audio_id, started_at, ended_at, content) {
    var uri = '/record/audio' + '?' + 'audio_id=' + audio_id;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', uri);
    xhr.send();
    xhr.onload = function() {
        var data_url = JSON.parse(xhr.responseText)['data_url'];
        audio.src = data_url;
        audio.currentTime = started_at / 1000.0;
        audio.volume = 1;
        audio.play();    
    };
};

var post_record_sentence_info = function(tmp_sentence_id, index, audio_id, started_at, ended_at, content) {
    var formData = new FormData();
    formData.append('index', index);
    formData.append('audio_id', audio_id);
    formData.append('started_at', started_at);
    formData.append('ended_at', ended_at);
    formData.append('content', content);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/record/sentence');
    xhr.send(formData);
    xhr.onload = function() {
        var sentence_id = JSON.parse(xhr.responseText)['sentence_id'];
        var sentence_tag = document.getElementById(tmp_sentence_id);
        // set real sentence id
        sentence_tag.id = sentence_id;
        sentence_tag.onclick = function(event) {
            get_audio_and_play(sentence_id, index, audio_id, started_at, ended_at, content);
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
            var current_tmp_id = current_start_tmp_id + i - 1
            var started_at = audio_timestamp[i-1];
            var ended_at = audio_timestamp[i];
            var sentence_tag = document.getElementById('tmp_' + current_tmp_id);
            var content = sentence_tag.textContent;
            
            post_record_sentence_info('tmp_' + current_tmp_id, i-1, audio_id, started_at, ended_at, content);
        }

        audio_timestamp = [];
    };
};

recordButton.onclick = function() {
    if(is_record == false) {
        is_record = true;
        console.log('Start');
        state_text.textContent = "Recording...";

        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(startRecording);
        recordButton.textContent = "STOP";
        recordButton.className = "btn btn-danger";
        
    }
    else {
        is_record = false;
        console.log('Stop');
        state_text.textContent = "";

        recognition.stop();
        recorder.stop();
        recordButton.textContent = "RECORD";
        recordButton.className = "btn btn-success";
    }
};

pauseButton.onclick = function() {
    audio.pause();
};