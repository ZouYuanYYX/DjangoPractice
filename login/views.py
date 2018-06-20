# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import sign
from merchant import get_id
from merchant import new_yiruku
from merchant import yikaidan
from merchant import yiruku
import mysql

# Create your views here.
def index(request):
    return render(request,"index.html")
#调登录接口
def login_action(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    merchantToken = sign.loginMerchant(username, password)
    return HttpResponse(merchantToken)

#获取发货网点信息
def getsendStation(request):
    data = request.POST
    mobile = data.get('mobile')
    merchantToken = data.get('merchantToken')
    result = mysql.getUserId(mobile)
    userId = result['id'].encode("utf-8")
    sendStation = get_id.getsendStation(merchantToken,userId)
    return HttpResponse(sendStation)

#获取收货网点信息
def getReceiverStation(request):
    data = request.POST
    mobile = data.get('mobile')
    merchantToken = data.get('merchantToken')
    result = mysql.getUserId(mobile)
    userId = result['id'].encode("utf-8")
    receiver = get_id.getReceiverStation(merchantToken,userId)
    return HttpResponse(receiver)
#创建托运单
def createTYD(request) :
    data = request.POST
    #从前端读取的值
    tydStatus = data.get('tydStatus')
    mobile = data.get('mobile')
    merchantToken = data.get('merchantToken')
    senderStation = data.get('senderStation')
    receiverStation = data.get('receiverStation')
    pickGoodsWay = data.get('pickGoodsWay')
    goodsName = data.get('goodsName')

    #后台需要处理的字段
    result = mysql.getUserId(mobile)
    userName = result['username'].encode("utf-8")
    userId = result['id'].encode("utf-8")
    #网点id
    sendStationId = mysql.getStationId(senderStation)
    receiveStationId = mysql.getStationId(receiverStation)

    print("托运单状态："+ tydStatus)
    if tydStatus == "已入库":
        if pickGoodsWay == "送货上门":
            tyd_id = new_yiruku.yiruku(merchantToken,userName,userId,pickGoodsWay,sendStationId,senderStation,receiveStationId,receiverStation,goodsName)
        else:
            tyd_id = yiruku.yiruku(merchantToken)


    if tydStatus == "已开单":
        tyd_id = yikaidan.yikaidan(merchantToken,userName,userId,pickGoodsWay,sendStationId,senderStation,receiveStationId,receiverStation,goodsName)
    return HttpResponse("托运单id为："+tyd_id)


