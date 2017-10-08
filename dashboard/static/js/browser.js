// JavaScript Document
function checkout_browser(){
    var Sys = {};
    var ua = navigator.userAgent.toLowerCase();
    var s;
    (s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] :

        (s = ua.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1] :

            (s = ua.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1] :

                (s = ua.match(/opera.([\d.]+)/)) ? Sys.opera = s[1] :

                    (s = ua.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1] : 0;

    if (!Sys.firefox && !Sys.chrome && !Sys.safari) {
        //if (!Sys.ie){
        window.location.href=constant_root_url+"/center/iebrowsers/";
    }
}

checkout_browser();