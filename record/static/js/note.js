var back_btn = document.getElementById("back_btn");
var save_btn = document.getElementById("save_btn");

back_btn.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/record/mylist');
    xhr.send();
    xhr.onload = function() {
        var res = JSON.parse(xhr.responseText);
        location.href = res.url;
    };
}