var home_btn = document.getElementById("home_btn");

home_btn.onclick = function() {
    location.href = "/";
};

function onSignIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/signin/oauth/google');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        redirect_url = JSON.parse(xhr.responseText)['redirect_url'];
        user_id = JSON.parse(xhr.responseText)['user_id'];
        location.href = "/static/mylist.html?user_id=" + user_id;
    };
    xhr.send('idtoken=' + id_token);
}