from django.shortcuts import render
from django.http import JsonResponse
import requests
import xhs.help
from xhs import XhsClient


def sign(uri, data=None, a1="", web_session=""):
    # 填写自己的 flask 签名服务端口地址
    res = requests.post("http://localhost:5005/sign",
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }


def get_data(request):
    cookie = "abRequestId=7bec26bc-b2f4-5911-9649-0b4470b5c136; a1=18f41658d58mpi3cuzqb5dy71oj2c0y42szjhkyys30000177402; webId=718ba3cebcf1a8c500fcf8d72b3ad227; gid=yYi4yK2jy0J0yYi4yK2YfMTv2Y6U3qS7uAD2uvMfvWylVVq8JS8v4x888yWW48J8WDDWyW0f; xsecappid=xhs-pc-web; webBuild=4.16.0; web_session=04006977c2df41af0b2b417e73344b0b6e7eac; unread={%22ub%22:%226641eb5a000000001e01f784%22%2C%22ue%22:%2266225223000000001c008c6c%22%2C%22uc%22:32}; websectiga=9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8; sec_poison_id=31759895-bd22-4cad-85a7-8bd3dcff2f00; acw_tc=48dc6eac7df92ffe3dd6f34247c6bab8819b958ad65d2e6f1c2b0b43aaf36053"
    xhs_client = XhsClient(cookie, sign=sign)
    # get note info
    note_info = xhs_client.get_note_by_keyword("北京路亚", 1, 20)
    result = []
    for each in note_info.get("items"):
        
        id = each.get("id")
        print(id)
        try:
            detail = xhs_client.get_note_by_id(id)
            result.append({
                "user_info":detail.get("user", {}),
                "title": detail.get("title", ""),
                "detail": detail.get("desc", "")
            })
        except Exception as e:
            print(e)
    return JsonResponse({"data":result})