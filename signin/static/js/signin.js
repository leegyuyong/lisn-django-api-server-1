var home_btn = document.getElementById("home_btn");
var oauth_btn = document.getElementById("oauth_btn");

home_btn.onclick = function() {
    location.href = "/";
}
oauth_btn.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/record/mylist');
    xhr.send();
    xhr.onload = function() {
        var res = JSON.parse(xhr.responseText);
        location.href = res.url;
    };
}