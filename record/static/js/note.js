var back_btn = document.getElementById("back_btn");
var save_btn = document.getElementById("save_btn");
var user_title = document.getElementById("user_title");
var user_content = document.getElementById("user_text");
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
var note_id = getCookie('glisn_note_id');

var uri = '/record/note' + '?' + 'note_id=' + note_id;
var xhr = new XMLHttpRequest();
xhr.open('GET', uri);
xhr.send();
xhr.onload = function() {
    var note = JSON.parse(xhr.responseText);
    user_title.value = note['title'];
    user_content.value = note['content'];

    var audios = note['audios'];
    for(var i=0; i<audios.length; i++){
        var sentences = audios[i].sentences;
        for(var j=0; j<sentences.length; j++){
            var sentence = sentences[j];
            var sentence_tag = document.createElement('h4');
            var newline = document.createElement('hr');
            sentence_tag.id = sentence.sentence_id;
            sentence_tag.className = "audio_stt_result";
            sentence_tag.textContent = sentence.content;
            sentence_tag.style.color = '#000000';
            sentence_tag.dataset.started_at = sentence.started_at;
            sentence_tag.dataset.ended_at = sentence.ended_at;
            
            sentence_tag.onclick = function(event) {
                window.AudioContext = window.AudioContext||window.webkitAudioContext||window.mozAudioContext;
                var audio_context = new AudioContext();
                var source = audio_context.createBufferSource();

                var uri = '/record/sentence' + '?' + 'sentence_id=' + event.target.id;
                var xxxhr = new XMLHttpRequest();
                xxxhr.open('GET', uri);
                xxxhr.responseType = 'arraybuffer';
                xxxhr.send();
                xxxhr.onload = function() {
                    audio_context.decodeAudioData(xxxhr.response, function(buffer) {
                        source.buffer = buffer;
                        source.connect(audio_context.destination);
                        source.start(0);
                    }, null);
                };
            };

            sentence_list.appendChild(sentence_tag);
            sentence_list.appendChild(newline);
        }
    }
};

save_btn.onclick = function() {
    var note_id = getCookie('glisn_note_id');
    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('note_id', note_id);
    formData.append('title', user_title.value);
    formData.append('content', user_content.value);
    xhr.open('PUT', '/record/note');
    xhr.send(formData);
    xhr.onload = function() {
        console.log('title and content are saved!');
    }
};

back_btn.onclick = function() {
    var note_id = getCookie('glisn_note_id');
    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('note_id', note_id);
    formData.append('title', user_title.value);
    formData.append('content', user_content.value);
    xhr.open('PUT', '/record/note');
    xhr.send(formData);
    xhr.onload = function() {
        console.log('title and content are saved!');
        location.href = "/static/mylist.html";
    }
};