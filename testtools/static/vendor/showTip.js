//tip是提示信息，type:'success'是成功信息，'danger'是失败信息,'info'是普通信息
function ShowTip(tip, type) {
    var $tip = $('#tip');
    if ($tip.length == 0) {
        $tip = $('<span id="tip" style="font-weight:bold;position:absolute;margin-left:25%;\n' +
            '    margin-top:15%;top:50px;left:50%;z-index:9999"></span>');
        $('body').append($tip);
    }
    $tip.stop(true).attr('class', 'alert alert-' + type).text(tip).css('margin-left', -$tip.outerWidth() / 2).fadeIn(100).delay(1000).fadeOut(100);
}

function ShowMsg(msg) {
    ShowTip(msg, 'info');
}

function ShowSuccess(msg) {
    ShowTip(msg, 'success');
}

function ShowFailure(msg) {
    ShowTip(msg, 'danger');
}

function ShowWarn(msg, $focus, clear) {
    ShowTip(msg, 'warning');
    if ($focus) $focus.focus();
    if (clear) $focus.val('');
    return false;
}