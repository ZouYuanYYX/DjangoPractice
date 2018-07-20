# -*- coding:utf-8 -*-
# author 邹元
import interface
import time
import get_id
import json

#merchantToken：商户登陆后的token
#createrName：创建运单的用户名（即登陆的商户的用户名）
#createrId：创建运单的用户id
#takeGoodsMethod：提货方式
#sendStationId：发货网点id
#sendStationName：发货网点名
#receiveStationId：收货网点id
#receiveStationName：收货网点名
#goodsName：货物名称

def yikaidan(merchantToken,createrName,createrId,takeGoodsMethod,sendStationId,sendStationName,receiveStationId,receiveStationName,goodsName):
	'''获取托运单号及货号'''
	tyd_id = get_id.getTYD_id(merchantToken, sendStationId)
	tyh_id = get_id.getTYH_id(merchantToken, sendStationId)
	'''创建运单'''
	url = "http://192.168.173.152/api/operator/consign/add?token=" + merchantToken
	date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	consignBaseVo = {"gmtOrder": date,
					 "consignNo": tyd_id,
					 # '''createrName、createrId需要参数化'''
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
					 # '''sendStationId、sendStationName、receiveStationId、receiveStationName、takeGoodsMethod需要参数化'''
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
					 "id": "TYDB18061300438005A000"}
	consignGoodsInfoVoList = [{
		"id": "TYDH18061300259005A000",
		"consignBaseId": "TYDB18061300438005A000",
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
	r = interface.requestInterfacePost_Json(url, values)
	result = json.loads(r.decode())
	#定义接口的返回值
	kaiDanResult = {"status": 0, "message": '', "tydId": ''}
	if result['status'] == 200:
		kaiDanResult['status'] = result['status']
		kaiDanResult['message'] = result['message']
		kaiDanResult['tydId'] = tyd_id
	else:
		kaiDanResult['status'] = result['status']
		kaiDanResult['message'] = result['message']
		print "创建已开单状态的托运单失败！"
	return kaiDanResult