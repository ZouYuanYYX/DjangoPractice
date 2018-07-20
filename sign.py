# -*- coding:UTF-8 -*-
# author 邹元
import interface
import re

'''tms商户登陆'''
def loginMerchant(mobile,password):
    url = "http://192.168.173.152/api/auth/jwt/merchant/token"
    values = {"mobile":mobile, "password":password}
    '''调登录接口，获取返回结果'''
    response = interface.requestInterfacePost_Json(url, values)
    return response