import requests
from django.shortcuts import render


def index(request):
    return render(request, "index.html")

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

