# -*- coding:UTF-8 -*-
import interface
import re

'''tms商户登陆'''
def loginMerchant(mobile,password):
    url = "http://192.168.173.152/api/auth/jwt/merchant/token"
    values = {"mobile":mobile, "password":password}
    '''调登录接口，获取返回结果'''
    response = interface.requestInterfacePost_Json(url, values)
    print ("post请求获取的响应结果json类型:%s" % response)
    '''获取token并返回'''
    searchResult = re.search('"data":{"token":"(.*?)","loginNum"',response)
    print ("token为:%s" %searchResult.group(1))
    return searchResult.group(1)