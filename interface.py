# -*- coding:UTF-8 -*-
import requests
import json
'''get请求'''
def requestInterfaceGet(url):
    r = requests.get(url)
    print("获取返回的状态码:%s" %r.status_code)
    return r.content

'''请求头默认为:application/x-www-form-urlencoded'''
def requestInterfacePost(url,params):
    r = requests.post(url,data = params)
    print("获取返回的状态码:%s" %r.status_code)
    return r.content

'''请求格式为：application/json'''
def requestInterfacePost_Json(url,params):
    headers = {'content-type': 'application/json'}
    r = requests.post(url,data = json.dumps(params),headers=headers)
    print("获取返回的状态码:%s" %r.status_code)
    return r.content