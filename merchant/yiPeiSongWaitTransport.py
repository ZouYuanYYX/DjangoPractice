# -*- coding:utf-8 -*-
# author 邹元
import sys
import mysql
from merchant import createPeiSongDan
from merchant import yiDaoZhan

reload(sys)
sys.setdefaultencoding('utf8')

#已配送-待运输
#创建运输中状态的托运单，先创建托运单，再创建提货、分拨、配载单等，需要对配载单做发车动作
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yiPeiSongWaitTransport(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken,psdId,deliveryPoint) :

	deliveryPointId = mysql.getStationId(deliveryPoint)
	# 定义接口的返回值
	yiPeiSongWaitTransportResult = {"status": 0, "message": '', "tydId": ''}

	#创建已到货确认的托运单（已到站状态）
	yiDaoZhanResult = yiDaoZhan.yidaozhan(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken)
	if yiDaoZhanResult['status'] == 200:
		#创建配送单
		tydbId = mysql.getTydbId(yiDaoZhanResult['tydId'])
		createPeiSongDanResult = createPeiSongDan.createPeiSongDan(merchantToken, fbdToken, psdId, tydbId, createrName, createrId, deliveryPointId)
		if createPeiSongDanResult['status'] == 200:
			yiPeiSongWaitTransportResult['status'] = createPeiSongDanResult['status']
			yiPeiSongWaitTransportResult['message'] = createPeiSongDanResult['message']
			yiPeiSongWaitTransportResult['tydId'] = yiDaoZhanResult['tydId']
			print("已配送状态的托运单创建成功（配送单待运输）")
		else:
			yiPeiSongWaitTransportResult['status'] = createPeiSongDanResult['status']
			yiPeiSongWaitTransportResult['message'] = createPeiSongDanResult['message']
			print("配送单创建失败！")
	else:
		yiPeiSongWaitTransportResult['status'] = yiDaoZhanResult['status']
		yiPeiSongWaitTransportResult['message'] = yiDaoZhanResult['message']
		print("已配送状态的托运单创建失败（配送单待运输）")
	return yiPeiSongWaitTransportResult

