# -*- coding:utf-8 -*-
# author 邹元
#该方法为yunshuzhong的副本
import sys
import mysql
from merchant import new_YiRuKu
from merchant import yiRuKu
from merchant import createFenBoDan
from merchant import createPeiZaiDan

reload(sys)
sys.setdefaultencoding('utf8')

#创建运输中状态的托运单，先创建托运单，再创建提货、分拨、配载单等，需要对配载单做发车动作
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yunshuzhong(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken) :
	pzdRollOutId = mysql.getStationId(pzdRollOutPoint)
	pzdRollInPointId = mysql.getStationId(pzdRollInPoint)
	if generateFenBoDan == "否":
		if pickGoodsWay == "自送上门":
			#不创建分拨单，不创建提货单
			tyd_id = new_YiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId, sendStationName, receiveStationId, receiveStationName, goodsName)
			tydbId = mysql.getTydbId(tyd_id)
			#创建配载单
			createPeiZaiDan.createPeiZaiDan(merchantToken,pzdId,tydbId,createrName,createrId,pzdRollOutId,pzdRollOutPoint
											,pzdRollInPointId,pzdRollInPoint)
			#配载单发车
			createPeiZaiDan.pzd_yiFaChe(merchantToken,pzdId,pzdToken)

			print("不创建分拨单，不创建提货单")
		else :
			#不创建分拨单，要创建提货单
			tyd_id = yiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId, sendStationName, receiveStationId,
								   receiveStationName, goodsName, thdId, takeGoodsStation, takeGoodsStationId)
			tydbId = mysql.getTydbId(tyd_id)
			# 创建配载单
			createPeiZaiDan.createPeiZaiDan(merchantToken, pzdId, tydbId, createrName, createrId, pzdRollOutId,
											pzdRollOutPoint,pzdRollInPointId, pzdRollInPoint)
			# 配载单发车
			createPeiZaiDan.pzd_yiFaChe(merchantToken, pzdId,pzdToken)
			print("不创建分拨单，要创建提货单,再创建配载单")

	if generateFenBoDan == "是" :
		fbdRollOutPointId = mysql.getStationId(fbdRollOutPoint)
		fbdRollInPointId = mysql.getStationId(fbdRollInPoint)
		if pickGoodsWay == "自送上门":
			# 不创建提货单,直接创建已入库的托运单
			tyd_id = new_YiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId,
									   sendStationName, receiveStationId, receiveStationName, goodsName)
			tydbId = mysql.getTydbId(tyd_id)
			# 创建分拨单
			createFenBoDan.createFenBoDan(merchantToken,fbdToken, fbdId, tydbId, createrName, createrId, fbdRollOutPointId,
										fbdRollOutPoint,fbdRollInPointId, fbdRollInPoint)
			# 创建配载单
			createPeiZaiDan.createPeiZaiDan(merchantToken, pzdId, tydbId, createrName, createrId, pzdRollOutId,
											pzdRollOutPoint, pzdRollInPointId, pzdRollInPoint)
			# 配载单发车
			createPeiZaiDan.pzd_yiFaChe(merchantToken, pzdId,pzdToken)
			print("创建分拨单，不创建提货单")
		else:
			# 创建提货单,再创建已入库的托运单
			tyd_id = yiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId, sendStationName,
								   receiveStationId, receiveStationName, goodsName, thdId, takeGoodsStation, takeGoodsStationId)
			tydbId = mysql.getTydbId(tyd_id)
			# 创建分拨单
			createFenBoDan.createFenBoDan(merchantToken, fbdToken, fbdId, tydbId, createrName, createrId, fbdRollOutPointId,
											fbdRollOutPoint, fbdRollInPointId, fbdRollInPoint)
			# 创建配载单
			createPeiZaiDan.createPeiZaiDan(merchantToken, pzdId, tydbId, createrName, createrId, pzdRollOutId,
											pzdRollOutPoint, pzdRollInPointId, pzdRollInPoint)
			# 配载单发车
			createPeiZaiDan.pzd_yiFaChe(merchantToken, pzdId,pzdToken)
			print("创建分拨单，要创建提货单")


	return tyd_id
