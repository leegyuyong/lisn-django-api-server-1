var recordButton = document.getElementById('record_btn');
var audio_stt_result_list = document.getElementById('audio_stt_result_list');
var state_text = document.getElementById('state_text');

var is_record = false;
var recorder;
var chunks;
var tid;
var interval_secs = 5000;

var intervalRecording = function() {
    console.log('Sending...');
    state_text.textContent = "Sending...";
    recorder.stop();
    recorder.start();
    console.log('Recording...');
    state_text.textContent = "Recording...";
}

var startRecording = function(stream) {
    //init
    recorder = new MediaRecorder(stream);
    chunks = [];

    recorder.ondataavailable = function(e) {
        chunks.push(e.data);
    };

    recorder.onstop = function(e) {
        sendRecording();
    };

    tid = setInterval(intervalRecording, interval_secs);

    recorder.start();
    console.log('Start');
    state_text.textContent = "Recording...";
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
        var audio_stt_result = document.createElement('h3');
        audio_stt_result.className = "audio_stt_result";
        audio_stt_result.textContent = xhr.responseText;
        audio_stt_result_list.appendChild(audio_stt_result);
    };
};

recordButton.onclick = function() {
    if(is_record == false) {
        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(startRecording);
        recordButton.textContent = "STOP";
        recordButton.className = "btn btn-danger";
        is_record = true;
    }
    else {
        clearInterval(tid);
        console.log('Sending...');
        recorder.stop();
        console.log('Stop');
        state_text.textContent = "";

        recordButton.textContent = "RECORD";
        recordButton.className = "btn btn-success";
        is_record = false;
    }
};