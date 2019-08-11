var signout_btn = document.getElementById("signout_btn");
var create_note_btn = document.getElementById("create_note_btn");
var note_btn = document.getElementsByClassName("note_btn");

var setCookie = function(name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp*24*60*60*1000);
    document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
};
var getCookie = function(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
};
var user_id = getCookie('glisn_user_id');

var note_list = document.getElementById('note_list');
var uri = '/record/list' + '?' + 'user_id=' + user_id
var xhr = new XMLHttpRequest();
xhr.open('GET', uri);
xhr.send();
xhr.onload = function() {
    var mylist = JSON.parse(xhr.responseText);
    //console.log(xhr.responseText);
    var notes = mylist['notes'];
    for(var i=0; i<notes.length; i++){
        var li = document.createElement('li');
        var btn = document.createElement('button');
        btn.id = parseInt(notes[i].note_id);
        btn.type = "button";
        btn.className = "btn btn-outline-primary note_btn";
        btn.textContent = '[' + notes[i].title + ']\n';
        btn.textContent += notes[i].created_at + '\n';
        btn.onclick = function(event) {
            setCookie('glisn_note_id', event.target.id, 365);
            location.href = "/static/note.html";
        };

        var del_btn = document.createElement('button');
        del_btn.id = parseInt(notes[i].note_id);
        del_btn.type = "button";
        del_btn.className = "btn btn-outline-danger del_btn";
        del_btn.textContent = "Delete";
        del_btn.onclick = function(event) {
            var xhr = new XMLHttpRequest();
            var formData = new FormData();
            formData.append('note_id', event.target.id);
            xhr.open('DELETE', '/record/note');
            xhr.send(formData);
            xhr.onload = function() {
                //console.log(xhr.responseText);
                window.location.reload();
            };
        };

        li.appendChild(btn);
        li.appendChild(del_btn);
        note_list.appendChild(li);
    }
};

signout_btn.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/signin/token');
    xhr.send();
    xhr.onload = function() {
        var auth2 = gapi.auth2.getAuthInstance();
        setCookie('glisn_user_id', -1, 0);
        setCookie('glisn_note_id', -1, 0);
        auth2.signOut();
        auth2.disconnect();
        location.href = "/";
    }
};

create_note_btn.onclick = function() {
    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('user_id', user_id);
    xhr.open('POST', '/record/note');
    xhr.send(formData);
    xhr.onload = function() {
        var note_id = JSON.parse(xhr.responseText)['note_id'];
        setCookie('glisn_note_id', note_id, 365);
        location.href = "/static/note.html";
    };
};

window.onpageshow = function(event){
    var historyTraversal = event.persisted || 
    (typeof window.performance != "undefined" && window.performance.navigation.type === 2);
    if (historyTraversal){
      window.location.reload();
    }
};