# -*- coding:utf-8 -*-
# author 邹元
import time
import interface
import mysql
import json

date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#新增配载单,tydbId格式类似：TYDB18070200442031A000
#pzdRollInPoint:配载单转入网点
#pzdRollInPointId:配载单转入网点id
#pzdRollOutPoint:配载单转出网点
#pzdRollOutId：配载单转出网点id
#merchantToken：商户登陆后的token
#pzdId：配载单id
#createrName：创建运单的用户名（即登陆的商户的用户名）
#createrId：创建运单的用户id
def createPeiZaiDan(merchantToken,pzdId,tydbId,createrName,createrId,pzdRollOutId,pzdRollOutPoint,pzdRollInPointId,pzdRollInPoint) :
	'''创建运单'''
	url = "http://192.168.173.152/api/operator/stowage/save?token=" + merchantToken
	values = {
		"stowageNo": pzdId,
		"driverId": "SJ18051700046002A000",
		"driverName": "邹元司机2",
		"driverPhone": "13003641778",
		"trunkId": "TRUCK18051000044001A000",
		"trunkNo": "浙B11123",
		"trailerNo": "",
		"transportFee": 52.69,
		"cashPay": 12.5,
		"collectPay": 10.5,
		"receiptPay": 1,
		"handlingFee": 0,
		"preOilCard": 2,
		"createrName": createrName,
		"createrId": createrId,
		"remark": "",
		"gmtStowageOrder": date,
		"gmtSendCar": date,
		"rollInStationId": pzdRollInPointId,
		"rollInStationName": pzdRollInPoint,
		"rollOutStationId": pzdRollOutId,
		"rollOutStationName": pzdRollOutPoint,
		"totalFee": 0,
		"relationVoList": [{
			"consignBaseId": tydbId,
			"amount": 9
		}]
	}
	r = interface.requestInterfacePost_Json(url, values)
	peiZaiDanResult = json.loads(r.decode())
	# 定义接口的返回值
	createPeiZaiDanResult = {"status": 0, "message": ''}
	if peiZaiDanResult['status'] == 200:
		createPeiZaiDanResult['status'] = peiZaiDanResult['status']
		createPeiZaiDanResult['message'] = peiZaiDanResult['message']
		print "配载单创建成功！"
	else:
		createPeiZaiDanResult['status'] = peiZaiDanResult['status']
		createPeiZaiDanResult['message'] = peiZaiDanResult['message']
		print "配载单创建失败！"

	return createPeiZaiDanResult


#配载单发车,传参的配载单id：PZD18070300146001A000
def pzd_yiFaChe(merchantToken,pzdId,pzdToken):
	# 定义接口的返回值
	pzdFaCheResult = {"status": 0, "message": ''}
	pzdbId = mysql.getPzdbId(pzdId)
	if pzdToken == '':
		url = "http://192.168.173.152/api/operator/stowage/sendCar?token=" + merchantToken
	else :
		url = "http://192.168.173.152/api/operator/stowage/sendCar?token=" + pzdToken
	values = {
		"id": pzdbId
	}
	# 配载单发车
	r = interface.requestInterfacePost_Json(url,values)
	faCheResult = json.loads(r.decode())
	if faCheResult['status'] == 200:
		pzdFaCheResult['status'] = faCheResult['status']
		pzdFaCheResult['message'] = faCheResult['message']
		print "配载单发车成功"
	else:
		pzdFaCheResult['status'] = faCheResult['status']
		pzdFaCheResult['message'] = faCheResult['message']
		print "配载单发车失败"
	return pzdFaCheResult


#配载单到货确认，用户要有转入网点的权限，才能到货确认,tydbId:TYDB18070200442031A000
def pzd_yiDaoZhan(merchantToken,pzdId,tydbId,pzdToken):
	# 定义接口的返回值
	pzdDaoZhanResult = {"status": 0, "message": ''}
	pzdbId = mysql.getPzdbId(pzdId)
	if pzdToken == '':
		url = "http://192.168.173.152/api/operator/stowage/arrivalConfirm?token=" + merchantToken
	else:
		url = "http://192.168.173.152/api/operator/stowage/arrivalConfirm?token=" + pzdToken
	values = {
		"id": pzdbId,
		"gmtArrival": date,
		"remarkArrival": '',
		"relationVoList": [{
			"consignBaseId":tydbId ,
			"goodsLoss": 0
		}]
	}
	result = json.loads( (interface.requestInterfacePost_Json(url, values)).decode() )
	if result['status'] == 200:
		pzdDaoZhanResult['status'] = result['status']
		pzdDaoZhanResult['message'] = result['message']
		print "配载单到货确认成功"
	else:
		pzdDaoZhanResult['status'] = result['status']
		pzdDaoZhanResult['message'] = result['message']
		print "配载单到货确认失败"

	return pzdDaoZhanResult
