var recordButton = document.getElementById('record');
var stopButton = document.getElementById('stop');
var audioPlayer = document.getElementById('player');
var sttText = document.getElementById('stt_text');
recordButton.disabled = false;
stopButton.disabled = true;

var recorder;
var chunks;

var startRecording = function(stream) {

    // init
    recorder = new MediaRecorder(stream);
    chunks = [];

    recorder.ondataavailable = function(e) {
        chunks.push(e.data);
    };

    recorder.onstop = function(e) {
        sendRecording();
    };

    recorder.start();
    sttText.textContent = "Recording...";
    console.log('Start Recording...');
};

var sendRecording = function() {
    sttText.textContent = "Send Recording...";
    var blob = new Blob(chunks, {'type': 'audio/webm;'});
    var fileName = Date.now();

    // clear chunks
    chunks = [];
    // set HTML <audio>
    audioPlayer.src = URL.createObjectURL(blob);

    var formData = new FormData();
    formData.append('data', blob, fileName);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/record/');
    xhr.send(formData);
    xhr.onload = function() {
        sttText.textContent = xhr.responseText;
    };
    console.log('Stop and Send Recording...');
};

recordButton.onclick = function() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(startRecording);
    recordButton.disabled = true;
    stopButton.disabled = false;
};

stopButton.onclick = function() {
    recorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;
};