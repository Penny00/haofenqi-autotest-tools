function checkSelect(obj) {
    var val = obj.value;
    if(val == "") {
        return false; //不提交请求
    } else {
        return true; //提交请求，
    }
}

//提交校验
function dosubmit() {
var select1 = checkSelect(document.getElementById('caseName'));
var select2 = checkSelect(document.getElementById('node'));
var select3 = checkSelect(document.getElementById('key'));
var select4 = checkSelect(document.getElementById('port_key'));
var select5 = checkSelect(document.getElementById('account_key'));
var select6 = checkSelect(document.getElementById('java_key'));
if(select1 && select2 && select3 && select4 && select5 && select6) {
//提交表单代码
return true;
} else {
alert("存在未选择的条件");
return false; //停留在本页不提交
}
}




