# -*- coding:utf-8 -*-
# author 邹元

import interface
import re
'''获取托运单号'''
def getTYD_id(token,sendStationId):
    url = "http://192.168.173.152/api/operator/consign/buildNewConsignNo?sendStationId="+sendStationId+"&token="+token
    print("url:"+url)
    reponse = interface.requestInterfaceGet(url)
    print ("托运单号：%r"%re.search('"data":"(.*?)",',reponse))
    tyd_id = re.search('"data":"(.*?)",',reponse).group(1)
    print("托运单号为："+tyd_id)
    return tyd_id

'''获取货号'''
def getTYH_id(token,sendStationId):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/consign/buildNewConsignGoodsNo?sendStationId="+sendStationId+"&token="+token)
    tyh_id = re.search('"data":"(.*?)",',reponse).group(1)
    print("货号为："+tyh_id)
    return tyh_id

'''获取发货网点信息'''
def getsendStation(token,userId):
    print("userId：" +userId)
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/admin/organization/merchant/getStationByUserId?type=1&userId="+userId+"&token="+token)
    print("响应结果：" + reponse)
    return reponse

'''获取提货单信息'''
def getTiHuoDanId(token):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/takeGoods/getTakeGoodsNo?token="+token)
    print("响应结果：" + reponse)
    return reponse

'''获取分拨单id'''
def getFenBoDanId(token):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/separateList/addPage?token="+token)
    print("响应结果：" + reponse)
    return reponse

'''获取配载单id'''
def getPeiZaiDanId(token):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/stowage/getNewStowageNo?token="+token)
    print("响应结果：" + reponse)
    return reponse

'''获取配送单id'''
def getPeiSongDanId(token):
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/operator/deliver/buildNo?token="+token)
    print("响应结果：" + reponse)
    return reponse

'''获取收货网点信息'''
def getReceiverStation(token,userId):
    print("userId：" +userId)
    reponse = interface.requestInterfaceGet("http://192.168.173.152/api/admin/organization/merchant/getStationByUserId?type=3&userId="+userId+"&token="+token)
    return reponse
