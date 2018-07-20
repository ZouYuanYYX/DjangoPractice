# -*- coding:utf-8 -*-
# author 邹元
import time
import interface
import mysql
import json

date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


#新增配送单,tydbId:YDB18070200442031A000,psdId:QXWLPS180710001
#fbdRollInPointId:分拨单转入网点
#fbdRollOutPoint:分拨单转出网点
def createPeiSongDan(merchantToken,fbdToken,psdId,tydbId,createrName,createrId,deliveryPointId) :
	# 定义接口的返回值
	createPeiSongDanResult = {"status": 0, "message": ''}
	'''创建运单'''
	url = "http://192.168.173.152/api/operator/deliver/save?token=" + merchantToken
	values = {
		"stationId": deliveryPointId,
		"deliverDate": date,
		"deliverNo": psdId,
		"departDate": date,
		"createPerson": createrId,
		"createPersonName": createrName,
		"phone": "13003641778",
		"driverId": "SJ18051700046002A000",
		"carId": "浙A11111",
		"priceDeliver": "29.68",
		"billingUnit": "",
		"remarks": "",
		"remarkType": " 易碎;防潮;",
		"consigns": [{
			"consignId": tydbId,
			"consignAmount": 9,
			"totalConsignAmount": 9
		}]
	}
	result = json.loads( (interface.requestInterfacePost_Json(url, values)).decode()  )
	if result['status'] == 200:
		createPeiSongDanResult['status'] = result['status']
		createPeiSongDanResult['message'] = result['message']
		print "配送单创建成功"
	else:
		createPeiSongDanResult['status'] = result['status']
		createPeiSongDanResult['message'] = result['message']
		print "配送单创建失败"

	return createPeiSongDanResult

#配送单配送,直接传配载单用户的token，因为配载单转入网点与配送网点相同，
#有配载单转入网点的权限，就肯定有配送网点的权限
def peiSong (merchantToken,psdId,pzdToken) :
	# 定义接口的返回值
	peiSongResult = {"status": 0, "message": ''}
	# 配送单配送，用户要有配送网点的权限，才能配送,psdbId:DELI18060600327012A000
	psdbId = mysql.getPsdbId(psdId)
	if pzdToken == '':
		url = "http://192.168.173.152/api/operator/deliver/status/"+psdbId+"/ALREADY_STATR?token=" + merchantToken
	else :
		url = "http://192.168.173.152/api/operator/deliver/status/"+psdbId+"/ALREADY_STATR?token=" + pzdToken
	values = {}
	# 配送单配送
	result = json.loads( (interface.requestInterfacePut(url, values)).decode() )
	if result['status'] == 200:
		peiSongResult['status'] = result['status']
		peiSongResult['message'] = result['message']
		print "配送单配送成功"
	else:
		peiSongResult['status'] = result['status']
		peiSongResult['message'] = result['message']
		print "配送单配送失败"

	return peiSongResult
