# -*- coding: utf-8 -*-
# author 邹元
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
import sign
import json
from merchant import get_id
from merchant import new_YiRuKu
from merchant import yiKaiDan
from merchant import yiRuKu
from merchant import yiPeiZai
from merchant import yunShuZhong
from merchant import yiDaoZhan
from merchant import yiPeiSongWaitTransport
from merchant import yiPeiSongTransporting
from merchant import yiQianShou
import mysql

# Create your views here.
def index(request):
    return render(request,"index.html")
#调登录接口
def login_action(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    loginResponse = sign.loginMerchant(username, password)
    return HttpResponse(loginResponse)

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

#获取提货单信息
def getTiHuoDanId(request):
    data = request.POST
    merchantToken = data.get('merchantToken')
    receiver = get_id.getTiHuoDanId(merchantToken)
    return HttpResponse(receiver)

#获取分拨单id
def getFenBoDanId(request):
    data = request.POST
    merchantToken = data.get('merchantToken')
    receiver = get_id.getFenBoDanId(merchantToken)
    return HttpResponse(receiver)

#获取配载单id
def getPeiZaiDanId(request):
    data = request.POST
    merchantToken = data.get('merchantToken')
    receiver = get_id.getPeiZaiDanId(merchantToken)
    return HttpResponse(receiver)

#获取配送单id
def getPeiSongDanId(request):
    data = request.POST
    merchantToken = data.get('merchantToken')
    receiver = get_id.getPeiSongDanId(merchantToken)
    return HttpResponse(receiver)

#创建托运单
def createTYD(request) :
    data = request.POST
    #从前端读取的值
    tydStatus = data.get('tydStatus')
    #是否要生成分拨单
    createFenBoDan = data.get('createFenBoDan')
    # 是否要生成配送单
    createPeiSongDan = data.get('createPeiSongDan')
    #登陆用户的手机号
    mobile = data.get('mobile')
    #登陆用户的token
    merchantToken = data.get('merchantToken')
    #分拨单为了能收货登陆的用户
    fbdToken = data.get('fbdToken')
    #配载单为了能发车登陆的用户
    pzdToken = data.get('pzdToken')
    #发货网点
    senderStation = data.get('senderStation')
    #收货网点
    receiverStation = data.get('receiverStation')
    #提货方式
    pickGoodsWay = data.get('pickGoodsWay')
    #货物名称
    goodsName = data.get('goodsName')
    #提货单id
    thdId = data.get('thdId')
    #提货网点
    takeGoodsStation = data.get('takeGoodsStation')
    #配载单id
    pzdId = data.get('pzdId')
    #配载单转出网点
    pzdRollOutPoint = data.get('pzdSenderPoint')
    #配载单转入网点
    pzdRollInPoint = data.get('pzdReceiverPoint')
    #分拨单id
    fbdId = data.get('fbdId')
    # 分拨单转出网点
    fbdRollOutPoint = data.get('fbdSenderPoint')
    # 分拨单转入网点
    fbdRollInPoint = data.get('fbdReceiverPoint')
    #配送单id
    psdId = data.get('psdId')
    #配送网点
    deliveryPoint = data.get('deliveryPoint')

    #登陆用户的userName和userId
    result = mysql.getUserId(mobile)
    userName = result['username'].encode("utf-8")
    userId = result['id'].encode("utf-8")

    #网点id
    sendStationId = mysql.getStationId(senderStation)
    receiveStationId = mysql.getStationId(receiverStation)
    takeGoodsStationId = mysql.getStationId(takeGoodsStation)

    #定义接口返回给前端的值
    #result = {"status": 0, "message": '', "tydId": ''}

    print("托运单状态："+ tydStatus)
    if tydStatus == "已入库":
        if pickGoodsWay == "自送上门":
            result = new_YiRuKu.yiruku(merchantToken, userName, userId, pickGoodsWay, sendStationId, senderStation,
                                       receiveStationId, receiverStation, goodsName)
        else:
            result = yiRuKu.yiruku(merchantToken, userName, userId, pickGoodsWay, sendStationId, senderStation,
                                   receiveStationId, receiverStation, goodsName, thdId, takeGoodsStation,
                                   takeGoodsStationId)
    elif tydStatus == "已开单":
        result = yiKaiDan.yikaidan(merchantToken, userName, userId, pickGoodsWay, sendStationId, senderStation,
                                   receiveStationId, receiverStation, goodsName)

    elif tydStatus == "已配载":
        result = yiPeiZai.yipeizai(merchantToken, createFenBoDan, userName, userId, pickGoodsWay, sendStationId,
                                   senderStation, receiveStationId, receiverStation, goodsName, thdId, takeGoodsStation,
                                   takeGoodsStationId, pzdRollOutPoint, pzdRollInPoint, pzdId, fbdId, fbdRollOutPoint, fbdRollInPoint, fbdToken)
    elif tydStatus == "运输中":
        result = yunShuZhong.yunshuzhong(merchantToken, createFenBoDan, userName, userId, pickGoodsWay, sendStationId,
                                         senderStation, receiveStationId, receiverStation, goodsName, thdId, takeGoodsStation,
                                         takeGoodsStationId, pzdRollOutPoint, pzdRollInPoint, pzdId, fbdId, fbdRollOutPoint,
                                         fbdRollInPoint, fbdToken, pzdToken)
    elif tydStatus == "已到站":
        result = yiDaoZhan.yidaozhan(merchantToken, createFenBoDan, userName, userId, pickGoodsWay, sendStationId,
                                     senderStation, receiveStationId, receiverStation, goodsName, thdId, takeGoodsStation,
                                     takeGoodsStationId, pzdRollOutPoint, pzdRollInPoint, pzdId, fbdId, fbdRollOutPoint,
                                     fbdRollInPoint, fbdToken, pzdToken)
    elif tydStatus == "已配送(配送单待运输)":
        result = yiPeiSongWaitTransport.yiPeiSongWaitTransport(merchantToken, createFenBoDan, userName, userId, pickGoodsWay, sendStationId,
                                    senderStation, receiveStationId, receiverStation, goodsName, thdId,
                                    takeGoodsStation,
                                    takeGoodsStationId, pzdRollOutPoint, pzdRollInPoint, pzdId, fbdId, fbdRollOutPoint,
                                    fbdRollInPoint, fbdToken, pzdToken,psdId,deliveryPoint)
    elif tydStatus == "已配送(配送单运输中)":
        result = yiPeiSongTransporting.yiPeiSongTransporting(merchantToken, createFenBoDan, userName, userId, pickGoodsWay, sendStationId,
                                     senderStation, receiveStationId, receiverStation, goodsName, thdId,
                                     takeGoodsStation,
                                     takeGoodsStationId, pzdRollOutPoint, pzdRollInPoint, pzdId, fbdId, fbdRollOutPoint,
                                     fbdRollInPoint, fbdToken, pzdToken,psdId,deliveryPoint)
    elif tydStatus == "已签收":
        result = yiQianShou.yiQianShou(merchantToken, createFenBoDan, userName, userId, pickGoodsWay, sendStationId,
                                     senderStation, receiveStationId, receiverStation, goodsName, thdId,
                                     takeGoodsStation,takeGoodsStationId, pzdRollOutPoint, pzdRollInPoint, pzdId, fbdId, fbdRollOutPoint,
                                     fbdRollInPoint, fbdToken, pzdToken,psdId,deliveryPoint,createPeiSongDan)
    #result为字典格式，要转换成json格式返回给前端
    return HttpResponse(json.dumps(result),content_type="application/json")


