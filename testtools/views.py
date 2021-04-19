from django.shortcuts import render


import datetime

from run_all_case import create_Data
from common.database import mysql_Test
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import Node,Excutelog,Configfile,Interface,Interface_execute,Process_block_statistics
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse,FileResponse,JsonResponse
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializers import ProcessSerializer
import paramiko
import os,time
import requests
import json

def select_data(request):
    '''筛选数据'''
    nodes = Node.objects.all().order_by("-id")
    configfiles = Configfile.objects.all()
    context = {}
    context['nodes'] = nodes
    context['configfiles'] = configfiles
    return render(request, "autotest/create_data/index.html", context)

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
    sql_test = mysql_Test("database_172.16.2.153")
    select_id = "select uid from haohuan_db_dev.user_account m where m.account='{}' limit 1;".format(encrypt_inter(encrypt_str))
    select_result = sql_test.select_sql(select_id)
    if select_result is not None:
        uid = str(select_result['uid'])
        context["uid"] = uid
        sql_test = mysql_Test("database_172.16.2.153")
        select_id = "select name,pid from haohuan_db_dev.user_pid m where m.uid='{}' order by id desc  limit 1;".format(uid)
        select_result = sql_test.select_sql(select_id)
        if select_result is not None:
            name = decrypt_inter(str(select_result['name']))
            pid = decrypt_inter(str(select_result['pid']))
            context["name"] = name
            context["pid"] = pid
        sql_test = mysql_Test("database_172.16.2.153")
        select_id = "select bank_num from haohuan_db_dev.user_bank m where m.uid='{}' order by id desc limit 1;".format(uid)
        select_result = sql_test.select_sql(select_id)
        if select_result is not None:
            bank_num = decrypt_inter(str(select_result['bank_num']))
            context["bank_num"] = bank_num

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
    return render(request, "autotest/encrypt_decrypt/encrypt_decrypt.html", context)


