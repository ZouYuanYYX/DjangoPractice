# -*- coding:utf-8 -*-
# author 邹元
import time
import interface
import mysql
import json

date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


#新增分拨单,tydbId:YDB18070200442031A000,fbdId:FBD2018070300000004
#fbdRollInPointId:分拨单转入网点
#fbdRollOutPoint:分拨单转出网点
def createFenBoDan(merchantToken,fbdToken,fbdId,tydbId,createrName,createrId,fbdRollOutPointId,fbdRollOutPoint,fbdRollInPointId,fbdRollInPoint) :
	'''创建运单'''
	url = "http://192.168.173.152/api/operator/separateList/add?token=" + merchantToken
	values = {
		"separateNumber": fbdId,
		"separateType": "",
		"createPerson": createrName,
		"createPersonId": createrId,
		"carNumber": "浙A11111",
		"driver": "邹元司机",
		"phone": "15258824696",
		"amount": "",
		"weight": "",
		"volume": "",
		"shareType": 1,
		"consignNumber": "",
		"transferFee": 69,
		"nowFee": 1,
		"inFee": "",
		"returnFee": 68,
		"inCarFee": "",
		"outCarFee": "",
		"totalFee": 0,
		"waitSeparateTime": date,
		"deliveryStation": fbdRollOutPoint,
		"deliveryStationId": fbdRollOutPointId,
		"arrivalStation": fbdRollInPoint,
		"arrivalStationId": fbdRollInPointId,
		"loadingUnloadingGroup": "",
		"receiveStationName": fbdRollInPoint,
		"remark": "",
		"rightConsignList": [tydbId],
		"totalAmount": "9",
		"receiveStationId": fbdRollInPointId,
		"createrId": createrId,
		"totalWeight": "4.00",
		"totalVolume": "3.00",
		"gmtCreate": date,
		"createrName": createrName,
		"trunkNo": "浙A11111",
		"trunkId": "TRUCK18050900040002A000",
		"carryingCapacity": 5,
		"driverName": "邹元司机",
		"driverId": "SJ18051500042002A000",
		"driverPhone": "15258824696"
	}
	r = interface.requestInterfacePost_Json(url, values)

	# 分拨单收货接口的url，用户要有转入网点的权限，才能收货,fbdbId:SEPA18070300095002A000
	if fbdToken == '':
		url = "http://192.168.173.152/api/operator/separateList/receiveSeparate?token=" + merchantToken
	else :
		url = "http://192.168.173.152/api/operator/separateList/receiveSeparate?token=" + fbdToken

	# 定义接口的返回值
	createFenBoDanResult = {"status": 0, "message": ''}
	fenBoDanResult = json.loads(r.decode())
	if fenBoDanResult['status'] == 200:
		#如果分拨单创建成功，再对该分拨单做收货动作
		fbdbId = mysql.getFbdbId(fbdId)
		#分拨单收货的参数
		values = {"id": fbdbId}
		#调分拨单收货接口
		fbdConfirm = json.loads( (interface.requestInterfacePut(url, values)).decode() )
		if fbdConfirm['status'] == 200:
			createFenBoDanResult['status'] = fbdConfirm['status']
			createFenBoDanResult['message'] = fbdConfirm['message']
			print "分拨单创建、收货成功！"
		else:
			createFenBoDanResult['status'] = fbdConfirm['status']
			createFenBoDanResult['message'] = fbdConfirm['message']
			print "分拨单收货失败！"
	else:
		createFenBoDanResult['status'] = fenBoDanResult['status']
		createFenBoDanResult['message'] = fenBoDanResult['message']
		print "分拨单创建失败！"

	return createFenBoDanResult



