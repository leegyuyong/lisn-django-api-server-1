var signout_btn = document.getElementById("signout_btn");
var new_note_btn = document.getElementById("new_note_btn");
var note_btn = document.getElementsByClassName("note_btn");


signout_btn.onclick = function() {
    location.href = "/";
}

new_note_btn.onclick = function() {
    location.href = "/record/note";
};

for(var i = 0; i < note_btn.length; i++) {
    note_btn[i].onclick = function() {
        location.href = "/record/note";
    };
}