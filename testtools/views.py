import requests
from django.shortcuts import render
from common.database import MysqlTest


def index(request):
    return render(request, "index.html")


def userinfo(request):
    mobile = request.POST.get('mobile')
    context = {}
    context["mobile"] = mobile
    context["uid"] = None
    context["name"] = None
    context["pid"] = None
    context["system_unique_id"] = None
    context["audit_id"] = None
    context["loan_id"] = None

    #从数据库获取数据
    sql_test = MysqlTest()
    select_id = "select uid,system_unique_id from user_account where account='{}' limit 1".format(encrypt_inter(mobile))
    select_result = sql_test.select_sql(select_id)
    if select_result is not None:
        uid = select_result['uid']
        system_unique_id = select_result['system_unique_id']
        context["uid"] = uid
        context["system_unique_id"] = system_unique_id
        sql_test = MysqlTest()
        select_id = "select name,pid from user_pid where uid='{}' limit 1".format(uid)
        select_result = sql_test.select_sql(select_id)
        if select_result is not None:
            name = decrypt_inter(select_result['name'])
            pid = decrypt_inter(select_result['pid'])
            context["name"] = name
            context["pid"] = pid
        sql_test = MysqlTest()
        select_id = "select audit_id from user_audit where uid='{}' limit 1".format(uid)
        select_result = sql_test.select_sql(select_id)
        if select_result is not None:
            audit_id = select_result['audit_id']
            context["audit_id"] = audit_id
        sql_test = MysqlTest()
        select_id = "select loan_id from template_log where uid='{}' limit 1".format(uid)
        select_result = sql_test.select_sql(select_id)
        if select_result is not None:
            loan_id = select_result['loan_id']
            context["loan_id"] = loan_id
            
 #   print(context)
    return render(request, "verify_callback.html", context)








def encrypt_inter(encrypt_str):
    url = "http://172.16.2.131:9090/encrypt"
    param = {
        "account": "{}".format(encrypt_str)
    }
    res = requests.get(url, params=param)
    encrypt_after = res.content.decode("utf-8")
    return encrypt_after


def decrypt_inter(decrypt_str):
    url = "http://172.16.2.131:9090/decrypt"
    param = {
        "account": "{}".format(decrypt_str)
    }
    res = requests.get(url, params=param)
    decrypt_after = res.content.decode("utf-8")
    return decrypt_after


def encrypt_str(request):
    '''字符串加密'''
    encrypt_str = request.POST.get('encrypt_str')
    encrypt_after = encrypt_inter(encrypt_str)
    context = {}
    context["encrypt_str"] = encrypt_str
    context["encrypt_after"] = encrypt_after

    return render(request, "encrypt_decrypt.html", context)


def decrypt_str(request):
    '''字符串解密'''
    decrypt_str = request.POST.get('decrypt_str')
    url = "http://172.16.2.131:9090/decrypt"
    param = {
        "account": "{}".format(decrypt_str)
    }
    res = requests.get(url, params=param)
    decrypt_after = res.content.decode("utf-8")
    context = {}
    context["decrypt_str"] = decrypt_str
    context["decrypt_after"] = decrypt_after
    return render(request, "encrypt_decrypt.html", context)


#if __name__ == '__main__':
#    userinfo(13900000001)
