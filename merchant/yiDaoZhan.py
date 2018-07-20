# -*- coding:utf-8 -*-
# author 邹元
import sys
import mysql
from merchant import createPeiZaiDan
from merchant import yunShuZhong

reload(sys)
sys.setdefaultencoding('utf8')

#创建运输中状态的托运单，先创建托运单，再创建提货、分拨、配载单等，需要对配载单做发车动作
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yidaozhan(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken) :

	# 定义接口的返回值
	yiDaoZhanResult = {"status": 0, "message": '', "tydId": ''}
	#创建已发车状态的配载单
	yunShuZhongResult = yunShuZhong.yunshuzhong(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken)
	if yunShuZhongResult['status'] == 200:
		#配载单到货确认
		tydbId = mysql.getTydbId(yunShuZhongResult['tydId'])
		pzdDaoZhanResult = createPeiZaiDan.pzd_yiDaoZhan(merchantToken, pzdId, tydbId, pzdToken)
		if pzdDaoZhanResult['status'] == 200:
			yiDaoZhanResult['status'] = pzdDaoZhanResult['status']
			yiDaoZhanResult['message'] = pzdDaoZhanResult['message']
			yiDaoZhanResult['tydId'] = yunShuZhongResult['tydId']
			print("已到站状态的托运单创建成功")
		else:
			yiDaoZhanResult['status'] = pzdDaoZhanResult['status']
			yiDaoZhanResult['message'] = pzdDaoZhanResult['message']
			print("配载单到货确认失败")
	else:
		yiDaoZhanResult['status'] = yunShuZhongResult['status']
		yiDaoZhanResult['message'] = yunShuZhongResult['message']
		print("已到站状态的托运单创建失败")
	return yiDaoZhanResult





