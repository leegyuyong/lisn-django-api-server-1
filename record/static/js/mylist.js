var signout_btn = document.getElementById("signout_btn");
var create_note_btn = document.getElementById("create_note_btn");
var note_btn = document.getElementsByClassName("note_btn");

function get_url_params()
{
    var params = []
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for(var i=0; i<hashes.length; i++)
	{
	    var hash = hashes[i].split('=');
	    params.push(hash[0]);
	    params[hash[0]] = hash[1];
	}
	return params;
};

var params = get_url_params();
var user_id = params['user_id'];

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
            location.href = "/static/note.html?note_id=" + event.target.id;
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
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut();
    auth2.disconnect();
    location.href = "/";
};

create_note_btn.onclick = function() {
    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('user_id', user_id);
    xhr.open('POST', '/record/note');
    xhr.send(formData);
    xhr.onload = function() {
        //console.log(xhr.responseText);
        var note_id = JSON.parse(xhr.responseText)['note_id'];
        location.href = "/static/note.html?note_id=" + note_id;
    };
};

window.onpageshow = function(event){
    var historyTraversal = event.persisted || 
    (typeof window.performance != "undefined" && window.performance.navigation.type === 2);
    if (historyTraversal){
      window.location.reload();
    }
};