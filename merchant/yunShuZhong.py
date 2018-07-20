# -*- coding:utf-8 -*-
# author 邹元
import sys
from merchant import createPeiZaiDan
from merchant import yiPeiZai

reload(sys)
sys.setdefaultencoding('utf8')

#创建运输中状态的托运单，先创建托运单，再创建提货、分拨、配载单等，需要对配载单做发车动作
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yunshuzhong(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken) :

	# 定义接口的返回值
	yunShuZhongResult = {"status": 0, "message": '', "tydId": ''}
	#创建已配载状态的配载单
	peiZaiResult = yiPeiZai.yipeizai(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken)
	if peiZaiResult['status'] == 200:
		# 配载单发车
		pzdFaCheResult = createPeiZaiDan.pzd_yiFaChe(merchantToken, pzdId, pzdToken)
		if pzdFaCheResult['status'] == 200:
			yunShuZhongResult['status'] = pzdFaCheResult['status']
			yunShuZhongResult['message'] = pzdFaCheResult['message']
			yunShuZhongResult['tydId'] = peiZaiResult['tydId']
			print "配载单发车成功，运输中状态的托运单创建成功！"
		else:
			yunShuZhongResult['status'] = pzdFaCheResult['status']
			yunShuZhongResult['message'] = pzdFaCheResult['message']
			print "配载单发车失败！"
	else:
		yunShuZhongResult['status'] = peiZaiResult['status']
		yunShuZhongResult['message'] = peiZaiResult['message']
		print "运输中状态的配载单生成失败！"

	return yunShuZhongResult





