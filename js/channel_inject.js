function input_sms(sms_code) {
    var sms_input = document.getElementsByClassName("aq_def_overlay")[0].children[0].contentWindow.document.getElementsByClassName('J_SafeCode')[0]
    if (sms_input) {
        sms_input.value = sms_code
    }
    setTimeout(confirm_sms, 3000)
}

function confirm_sms() {
    var sms_confirm = document.getElementsByClassName("aq_def_overlay")[0].children[0].contentWindow.document.getElementById('J_FooterSubmitBtn')
    if (sms_confirm) {
        sms_confirm.click()
    }
}

new QWebChannel(qt.webChannelTransport, function (channel) {
    channel.objects.sms_code.mySignal.connect(function (result) {
        window.sms_code = channel.objects.sms_code
        alert(result)
        input_sms(result)
        channel.objects.sms_code.resultValue = "loginSuccess"
    })
    // window.sms_code = channel.objects.sms_code
    //alert('111 chanel='+channel)
    // window.sms_code = channel.objects.sms_code;
    // alert('sms_code=' + sms_code.strValue + '\n从pyqt传来的参数=' + window.sms_code.strValue);
    //alert('111 chanel='+ channel.objects.strValue)
})