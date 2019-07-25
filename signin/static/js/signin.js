var home_btn = document.getElementById("home_btn");
var oauth_btn = document.getElementById("oauth_btn");

home_btn.onclick = function() {
    location.href = "/";
}
oauth_btn.onclick = function() {
    location.href = "/record/mylist";
}