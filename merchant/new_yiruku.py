# -*- coding:utf-8 -*-
# author 邹元
import time
import interface
import get_id
import json

#提货方式为送货上门
def yiruku(merchantToken,createrName,createrId,takeGoodsMethod,sendStationId,sendStationName,receiveStationId,receiveStationName,goodsName) :
	'''获取托运单号及货号'''
	tyd_id = get_id.getTYD_id(merchantToken,sendStationId)
	tyh_id = get_id.getTYH_id(merchantToken,sendStationId)
	# 定义接口的返回值
	ruKuResult = {"status": 0, "message": '', "tydId": ''}
	date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	'''创建运单'''
	url = "http://192.168.173.152/api/operator/consign/add?token=" + merchantToken
	consignBaseVo = {"gmtOrder": date,
				"consignNo": tyd_id,
				"createrName": createrName,
				"createrId": createrId,
				"consignGoodsNo": tyh_id,
				"sender": "啦啦啦",
				"receiver": "南湖",
				"senderPhone": "15912121212",
				"receiverPhone": "19912345678",
				"sendRegionId": "360828",
				"sendRegionSpell": "江西省吉安万安县",
				"sendDetailAddress": "你就1231231232",
				"receiveRegionId": "230881",
				"receiveRegionSpell": "黑龙江省佳木斯同江市",
				"receiveDetailAddress": "你就",
				"sendStationId": sendStationId,
				"sendStationName": sendStationName,
				"receiveStationId": receiveStationId,
				"receiveStationName": receiveStationName,
				"takeGoodsMethod": takeGoodsMethod,
				"receiveGoodsMethod": "DTD_DELIVERY",
				"receiptRequire": "回单签字",
				"transportFee": 65,
				"infoFee": 10,
				"spotTransportFee": 10,
				"supportValueFee": 10,
				"collectionGoodsFee": 0,
				"collectionTransportFee": 0,
				"spotGoodsFee": 0,
				"takeGoodsFee": 40,
				"sendGoodsFee": 0,
				"otherFee": 0,
				"handlingFee": 50,
				"packingFee": 0,
				"upstairsFee": 10,
				"totalFee": "195.00",
				"payType": "现付",
				"cashPay": 0,
				"collectPay": 0,
				"receiptPay": 195,
				"monthPay": 0,
				"remark": "",
				"senderId": "CUS18060400081009A000",
				"receiverId": "CUS18060400081011A000",
				"remarkShort": " 易碎;防潮;",
				"consignSource": "BACKSTAGE_ADD",
				"id": "TYDB18060600428010A000"}
	consignGoodsInfoVoList = [{
		"id": "TYDH18060600254026A000",
		"consignBaseId": "TYDB18060600428010A000",
		"merchantId": "USER18050400072030A000",
		"goodsNo": "HH2018060400000049",
		"goodsName": goodsName,
		"goodsAmount": 9,
		"goodsAmountUnit": "件",
		"goodsWeight": 4,
		"goodsWeightUnit": "KG",
		"goodsVolume": 3, "goodsVolumeUnit": "MMM",
		"goodsType": "生活用品",
		"goodsPrice": 0,
		"goodsPriceUnit": "件",
		"goodsLoss": 0,
		"packageMethods": "木箱",
		"goodsAttribute": "抛货",
		"goodsImage": " ",
		"gmtCreate": date,
		"gmtModified": date,
		"visible": False}]

	values = {"consignBaseVo": consignBaseVo,
			"consignGoodsInfoVoList": consignGoodsInfoVoList}
	#调创建托运单的接口
	r = interface.requestInterfacePost_Json(url, values)
	createTydResult = json.loads(r.decode())
	if createTydResult['status'] == 200:
		ruKuResult['status'] = createTydResult['status']
		ruKuResult['message'] = createTydResult['message']
		ruKuResult['tydId'] = tyd_id
	else:
		ruKuResult['status'] = createTydResult['status']
		ruKuResult['message'] = createTydResult['message']
		print "托运单创建失败!"

	return ruKuResult



