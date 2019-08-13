var home_btn = document.getElementById("home_btn");

var setCookie = function(name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp*24*60*60*1000);
    document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
};
var getCookie = function(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
};

home_btn.onclick = function() {
    location.href = "/";
};

function onSignIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/v1/api/signin/oauth/google/user');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        redirect_url = JSON.parse(xhr.responseText)['redirect_url'];
        user_id = JSON.parse(xhr.responseText)['user_id'];
        setCookie('glisn_user_id', user_id, 365);
        location.href = "/static/mylist.html";
    };
    xhr.send('idtoken=' + id_token);
}