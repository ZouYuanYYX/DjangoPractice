# -*- coding:utf-8 -*-
import login
import json
import interface
import re
'''获取托运单号'''
def getTYD_id(token):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/consign/buildConsignNo?token="+token)
    tyd_id = re.search('"data":"(.*?)",',reponse).group(1)
    print("托运单号为："+tyd_id)
    return tyd_id

'''获取货号'''
def getTYH_id(token):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/consign/buildConsignGoodsNo?token="+token)
    tyh_id = re.search('"data":"(.*?)",',reponse).group(1)
    print("货号为："+tyh_id)
    return tyh_id

'''获取发货网点信息'''
def getsendStation(token,userId):
    print("userId：" +userId)
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/admin/organization/merchant/getStationByUserId?type=1&userId="+userId+"&token="+token)
    print("响应结果：" + reponse)
    return reponse

'''获取收货网点信息'''
def getReceiverStation(token,userId):
    print("userId：" +userId)
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/admin/organization/merchant/getStationByUserId?type=3&userId="+userId+"&token="+token)
    print("响应结果：" + reponse)
    return reponse
