var signin_btn = document.getElementsByClassName("signin_btn");
for(var i = 0; i < signin_btn.length; i++) {
    signin_btn[i].onclick = function() {
        location.href = "/signin/page";
    };
}