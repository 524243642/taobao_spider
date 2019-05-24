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
    var dx = rd(200, 300);
    var dy = rd(200, 300);
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, dx, dy, dx, dy, false, false, false, false, 0, null);
}

function username() {
    var mDown = document.createEvent("MouseEvents");
    var dx = rd(1, 5);
    var dy = rd(1, 5);
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, dx, dy, dx, dy, false, false, false, false, 0, null);

    document.getElementById('username').dispatchEvent(mDown);
    document.getElementById('username').value = '%s';
    setTimeout(password, 2000);
}

function password() {
    var mDown = document.createEvent("MouseEvents");
    var dx = rd(1, 5);
    var dy = rd(1, 5);
    mDown.initMouseEvent("mousedown", true, true, document.defaultView, 0, dx, dy, dx, dy, false, false, false, false, 0, null);
    document.getElementById('password').dispatchEvent(mDown);
    document.getElementById('password').value = '%s';
    // setTimeout(confirm, 2000);
}

// function verify() {
//     if (document.getElementsByClassName("km-dialog-btn").length > 0) {
//         var click_ele = document.getElementsByClassName("km-dialog-btn")[0];
//         if (click_ele) {
//             click_ele.click();
//         }
//     }
//
//     var click_span = document.getElementById("SM_TXT_1");
//     click_span.click();
//     setTimeout(confirm, 4000);
// }

// function confirm() {
//     var drag_div = document.getElementById("SM_TXT_1");
//     if (drag_div) {
//         verify();
//     }
//     setTimeout(confirm_success, 3000);
// }

// function confirm_success() {
//     document.getElementById('btn-submit').click();
// }

// function refresh() {
//     if (document.getElementsByClassName("error-refresh-button").length > 0) {
//         var click_ele = document.getElementsByClassName("error-refresh-button")[0];
//         if (click_ele) {
//             alert('refresh error page')
//             click_ele.click()
//         }
//     }
// }

function delay() {

}

function handle(path) {
    setTimeout(delay, 3000);
    setTimeout(username, 3000);
    mousewheel();
    // setTimeout(refresh, 3000)
}

//https://main.m.taobao.com/mytaobao/index.html
let host = document.location.hostname;
if (host.endsWith('.taobao.com')) {
    handle(document.location.pathname);
}

// function refresh() {
//     if (document.getElementsByClassName("error-refresh-button").length > 0) {
//         var click_ele = document.getElementsByClassName("error-refresh-button")[0];
//         if (click_ele) {
//             alert('refresh error page');
//             click_ele.click();
//         }
//     }
// }
//
// document.addEventListener("DOMContentLoaded", function () {
//     alert('load success');
//     // setTimeout(empty, 3000)
//     // alert(document.getElementsByClassName("aq_def_overlay").length)
//     // alert(window.document.getElementsByClassName("aq_def_overlay").length)
//     if (document.getElementsByClassName("error-refresh-button")) {
//         setTimeout(refresh, 3000);
//     }
// });