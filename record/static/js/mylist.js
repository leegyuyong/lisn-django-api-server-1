var signout_btn = document.getElementById("signout_btn");
var create_note_btn = document.getElementById("create_note_btn");
var note_btn = document.getElementsByClassName("note_btn");


signout_btn.onclick = function() {
    location.href = "/";
}

create_note_btn.onclick = function() {
    location.href = "/static/note.html";
};

for(var i = 0; i < note_btn.length; i++) {
    note_btn[i].onclick = function() {
        location.href = "/static/note.html";
    };
}