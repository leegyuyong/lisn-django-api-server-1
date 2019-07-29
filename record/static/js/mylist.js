var signout_btn = document.getElementById("signout_btn");
var create_note_btn = document.getElementById("create_note_btn");
var note_btn = document.getElementsByClassName("note_btn");


signout_btn.onclick = function() {
    location.href = "/";
}

create_note_btn.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/record/note');
    xhr.send();
    xhr.onload = function() {
        var res = JSON.parse(xhr.responseText);
        location.href = res.url;
    };
};

for(var i = 0; i < note_btn.length; i++) {
    note_btn[i].onclick = function() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/record/note');
        xhr.send();
        xhr.onload = function() {
            var res = JSON.parse(xhr.responseText);
            location.href = res.url;
        };
    };
}