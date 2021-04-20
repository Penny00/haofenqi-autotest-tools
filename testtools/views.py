#from django.shortcuts import render


#import datetime

from service.database import mysql_Test
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
#from .models import Node,Excutelog,Configfile,Interface,Interface_execute,Process_block_statistics
#from dwebsocket.decorators import accept_websocket, require_websocket
#from django.http import HttpResponse,FileResponse,JsonResponse
#from django.core.paginator import Paginator
#from rest_framework import status
#from rest_framework.decorators import api_view
#from rest_framework.renderers import JSONRenderer
#from rest_framework.response import Response
#from .serializers import ProcessSerializer
#import paramiko
#import os,time
import requests
#import json


class User(object):
    def __init__(self, account):
        self.account = account
        ret = mysqldb.sqlhelper.fetch_all(
            "SELECT account.system_unique_id,audit.audit_id,account.uid FROM user_account "
            "account LEFT JOIN user_audit  audit "
            "ON account.uid = audit.uid WHERE account.account = %s "
            "ORDER BY audit.id DESC LIMIT 1", (self.account,))
        self.user_info = dict2obj(ret[0]) if ret else None

    def uid(self):
        return self.user_info.uid

    def user_key(self):
        return self.user_info.system_unique_id

    def audit_id(self):
        return self.user_info.audit_id


def verify_callback():
    if request.method == "OPTIONS":
        return respons_json({})
    req_data = request.json
    account = CommonUtils.get_encrypt_data(req_data.get("account"))
    accept = req_data.get("accept")
    reject = req_data.get("reject")
    env = req_data.get("env")
    print(req_data)
    # type 0 认证审核回调, 1 借款审核回调, 2 交易审核回调
    type = req_data.get("type")

    is_accept = ("ACCEPT" if accept == 1 and reject == 0 else "REJECT")
    resp_data = {}

    result = ''
    if type == 0:
        result = VerifyCallback(account).auth_verify_callback(is_accept)
    elif type == 1:
        result = VerifyCallback(account).lend_verify_callback(is_accept, env)

    if result:
        if json.loads(result)["data"]["retCode"] == "00S0000":
            resp_data["data"] = {"result": 1}
        else:
            resp_data["data"] = {"result": 0}
        resp_data["code"] = 0
    return respons_json(resp_data)


@callback_bp.route('/callback/lending-notice', methods=("POST", "OPTIONS", 'GET'))
def lending_notice_callback():
    if request.method == "OPTIONS":
        return respons_json({})
    data = request.json or request.args
    if request.method == 'POST':
        if not data or data.get('data', None) is None or data.get('data').get('loanId') is None:
            return respons_json({'message': '必传字段loanId不存在或值为空, {\'data\':{\'loanId\':\'xxxx\'}}'})
        return lending_notice(data.get('data').get('loanId'))
    else:
        return respons_json({'data': lending_notice(data.get('loanId')),
                        'message': '不需要关注返回值， 直接在 http://haofenqi-contract-admin.test.rrdbg.com/main/index.do 平台上按时间查询是否重新生成协议'}
                       )


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
    context["uid"] = None
    context["name"] = None
    context["pid"] = None
    context["bank_num"] = None

    #数据库获取数据
    # sql_test = mysql_Test()
    # select_id = "select uid from haohuan_db_dev.user_account m where m.account='{}' limit 1;".format(encrypt_inter(encrypt_str))
    # select_result = sql_test.select_sql(select_id)
    # if select_result is not None:
    #     uid = str(select_result['uid'])
    #     context["uid"] = uid
    #     sql_test = mysql_Test()
    #     select_id = "select name,pid from haohuan_db_dev.user_pid m where m.uid='{}' order by id desc  limit 1;".format(uid)
    #     select_result = sql_test.select_sql(select_id)
    #     if select_result is not None:
    #         name = decrypt_inter(str(select_result['name']))
    #         pid = decrypt_inter(str(select_result['pid']))
    #         context["name"] = name
    #         context["pid"] = pid
    #     sql_test = mysql_Test()
    #     select_id = "select bank_num from haohuan_db_dev.user_bank m where m.uid='{}' order by id desc limit 1;".format(uid)
    #     select_result = sql_test.select_sql(select_id)
    #     if select_result is not None:
    #         bank_num = decrypt_inter(str(select_result['bank_num']))
    #         context["bank_num"] = bank_num

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


