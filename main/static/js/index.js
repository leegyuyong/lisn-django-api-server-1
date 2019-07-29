var signin_btn = document.getElementsByClassName("signin_btn");
for(var i = 0; i < signin_btn.length; i++) {
    signin_btn[i].onclick = function() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/signin/page');
        xhr.send();
        xhr.onload = function() {
            var res = JSON.parse(xhr.responseText);
            location.href = res.url;
        };
    };
}