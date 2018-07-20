# -*- coding:utf-8 -*-
# author 邹元
import sys
import mysql
from merchant import yiDaoZhan
from merchant import yiPeiSongTransporting
import interface
import json

reload(sys)
sys.setdefaultencoding('utf8')

#已签收
#创建运输中状态的托运单，先创建托运单，再创建提货、分拨、配载单等，需要对配载单做发车动作
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yiQianShou(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken,psdId,deliveryPoint,createPeiSongDan) :
	# 定义接口的返回值
	yiQianShouResult = {"status": 0, "message": '', "tydId": ''}
	if createPeiSongDan == "是":
		yiPeiSongTransportingResult = yiPeiSongTransporting.yiPeiSongTransporting(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken,psdId,deliveryPoint)
		if yiPeiSongTransportingResult['status'] == 200:
			tydId = yiPeiSongTransportingResult['tydId']
			tydbId = mysql.getTydbId(tydId)
			#签收单签收
			qianShouResult = qianShouDanSave(merchantToken,pzdToken,tydbId,goodsName,tydId,sendStationId,receiveStationId)
			if qianShouResult['status'] == 200:
				yiQianShouResult['status'] = qianShouResult['status']
				yiQianShouResult['message'] = qianShouResult['message']
				yiQianShouResult['tydId'] = yiPeiSongTransportingResult['tydId']
				print("已签收状态的托运单创建成功")
			else:
				yiQianShouResult['status'] = qianShouResult['status']
				yiQianShouResult['message'] = qianShouResult['message']
				print("签收单签收失败！")
		else:
			yiQianShouResult['status'] = yiPeiSongTransportingResult['status']
			yiQianShouResult['message'] = yiPeiSongTransportingResult['message']
			print("已签收状态的托运单创建失败")


	else:
		yiDaoZhanResult = yiDaoZhan.yidaozhan(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken)
		if yiDaoZhanResult['status'] == 200:
			tydId = yiDaoZhanResult['tydId']
			tydbId = mysql.getTydbId(tydId)
			#签收单签收
			qianShouResult = qianShouDanSave(merchantToken,pzdToken,tydbId,goodsName,tydId,sendStationId,receiveStationId)
			if qianShouResult['status'] == 200:
				yiQianShouResult['status'] = qianShouResult['status']
				yiQianShouResult['message'] = qianShouResult['message']
				yiQianShouResult['tydId'] = yiDaoZhanResult['tydId']
				print("已签收状态的托运单创建成功")
			else:
				yiQianShouResult['status'] = qianShouResult['status']
				yiQianShouResult['message'] = qianShouResult['message']
				print("签收单签收失败！")
		else:
			yiQianShouResult['status'] = yiDaoZhanResult['status']
			yiQianShouResult['message'] = yiDaoZhanResult['message']
			print("已签收状态的托运单创建失败")
	return yiQianShouResult

def qianShouDanSave(merchantToken,pzdToken,tydbId,goodsName,tydId,sendStationId,receiveStationId) :
	qianShouResult = {"status": 0, "message": ''}
	if pzdToken == '':
		url = "http://192.168.173.152/api/operator/sign/save?token="+merchantToken
	else:
		url = "http://192.168.173.152/api/operator/sign/save?token=" + pzdToken
	values = {"consignId":tydbId,
			  "commodityName":goodsName,
			  "consignNo":tydId,
			  "stationId":sendStationId,
			  "receiveStationId":receiveStationId
			  }
	r = interface.requestInterfacePost_Json(url,values)
	result = json.loads(r.decode())
	if result['status'] == 200:
		qianShouResult['status'] = result['status']
		qianShouResult['message'] = result['message']
		print "签收单成功签收"
	else:
		qianShouResult['status'] = result['status']
		qianShouResult['message'] = result['message']
		print "签收失败"
	return qianShouResult

