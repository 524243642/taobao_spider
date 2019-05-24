/**
 * JS获取n至m随机整数
 * 琼台博客
 */
function rd(n, m) {
    var c = m - n + 1;
    return Math.floor(Math.random() * c + n);
}

function mousewheel() {
    var mDown = document.createEvent("MouseEvents");
    var dx = rd(200, 300)
    var dy = rd(200, 300)
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, dx, dy, dx, dy, false, false, false, false, 0, null);
}

function username() {
    var mDown = document.createEvent("MouseEvents");
    var dx = rd(1, 5)
    var dy = rd(1, 5)
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, dx, dy, dx, dy, false, false, false, false, 0, null);

    document.getElementById('TPL_username_1').dispatchEvent(mDown)
    document.getElementById('TPL_username_1').value = '%s';
    setTimeout(password, 2000)
}

function password() {
    var mDown = document.createEvent("MouseEvents");
    var dx = rd(1, 5)
    var dy = rd(1, 5)
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, dx, dy, dx, dy, false, false, false, false, 0, null);
    document.getElementById('TPL_password_1').dispatchEvent(mDown)
    document.getElementById('TPL_password_1').value = '%s';
    setTimeout(confirm, 2000)
}

function verify() {
    var drag_div = document.getElementById("nc_1_n1z");
    var divX = drag_div.style.clientX;
    var divY = drag_div.style.clientY;
    var divX_end = 207;
    var divY_end = 0;
    var mDown = document.createEvent("MouseEvents");
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, divX, divY, divX, divY, false, false, false, false, 0, null);
    drag_div.dispatchEvent(mDown);
    var mMove = document.createEvent("MouseEvents");
    mMove.initMouseEvent("mousemove", true, true, document.defaultView, 0, divX_end, divY_end, divX_end, divY_end, false, false, false, false, 0, null);
    drag_div.dispatchEvent(mMove);
    setTimeout(confirm, 2500)
}

function confirm() {
    var drag_div = document.getElementById("nc_1_n1z");
    if (drag_div) {
        verify()
    }
    setTimeout(confirm_success, 2000)
}

function confirm_success() {
    document.getElementById('J_SubmitStatic').click();
    // setTimeout(click_sms, 4000)
}

function delay() {

}

function handle(path) {
    setTimeout(delay, 3000)
    setTimeout(username, 3000)
    mousewheel()
}

//sycm.taobao.com/custom/login.htm
let host = document.location.hostname;
if (host.endsWith('.taobao.com')) {
    handle(document.location.pathname);
}