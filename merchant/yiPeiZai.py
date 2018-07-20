# -*- coding:utf-8 -*-
# author 邹元
import sys
import mysql
from merchant import new_YiRuKu
from merchant import yiRuKu
from merchant import createFenBoDan
from merchant import createPeiZaiDan

reload(sys)
sys.setdefaultencoding('utf8')

#创建已配载状态的托运单，先创建托运单，再创建提货、分拨、配载单等
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yipeizai(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken) :
	pzdRollOutId = mysql.getStationId(pzdRollOutPoint)
	pzdRollInPointId = mysql.getStationId(pzdRollInPoint)

	# 定义接口的返回值
	peiZaiResult = {"status": 0, "message": '', "tydId": ''}

	if generateFenBoDan == "否":
		if pickGoodsWay == "自送上门":
			#不创建分拨单，不创建提货单,创建托运单
			ruKuResult = new_YiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId, sendStationName, receiveStationId, receiveStationName, goodsName)
			if ruKuResult['status'] == 200:
				tydbId = mysql.getTydbId(ruKuResult['tydId'])
				#创建配载单
				createPeiZaiDanResult = createPeiZaiDan.createPeiZaiDan(merchantToken,pzdId,tydbId,createrName,createrId,pzdRollOutId,pzdRollOutPoint
											,pzdRollInPointId,pzdRollInPoint)
				if createPeiZaiDanResult['status'] == 200:
					peiZaiResult['status'] = createPeiZaiDanResult['status']
					peiZaiResult['message'] = createPeiZaiDanResult['message']
					peiZaiResult['tydId'] = ruKuResult['tydId']
					print("不创建分拨单，不创建提货单，已配载状态的托运单创建成功")
				else:
					peiZaiResult['status'] = createPeiZaiDanResult['status']
					peiZaiResult['message'] = createPeiZaiDanResult['message']
					print("不创建分拨单，不创建提货单，已配载状态的托运单创建失败")
			else:
				peiZaiResult['status'] = ruKuResult['status']
				peiZaiResult['message'] = ruKuResult['message']
				print("创建已配载状态的托运单时，托运单创建失败")

		else :
			#不创建分拨单，要创建提货单,创建托运单
			ruKuResult = yiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId, sendStationName, receiveStationId,
								   receiveStationName, goodsName, thdId, takeGoodsStation, takeGoodsStationId)
			if ruKuResult['status'] == 200:
				tydbId = mysql.getTydbId(ruKuResult['tydId'])
				# 创建配载单
				createPeiZaiDanResult = createPeiZaiDan.createPeiZaiDan(merchantToken, pzdId, tydbId, createrName, createrId, pzdRollOutId,
											pzdRollOutPoint,pzdRollInPointId, pzdRollInPoint)
				if createPeiZaiDanResult['status'] == 200:
					peiZaiResult['status'] = createPeiZaiDanResult['status']
					peiZaiResult['message'] = createPeiZaiDanResult['message']
					peiZaiResult['tydId'] = ruKuResult['tydId']
					print("不创建分拨单，要创建提货单，已配载状态的托运单创建成功")
				else:
					peiZaiResult['status'] = createPeiZaiDanResult['status']
					peiZaiResult['message'] = createPeiZaiDanResult['message']
					print("不创建分拨单，要创建提货单，已配载状态的托运单创建失败")

	if generateFenBoDan == "是" :
		fbdRollOutPointId = mysql.getStationId(fbdRollOutPoint)
		fbdRollInPointId = mysql.getStationId(fbdRollInPoint)
		if pickGoodsWay == "自送上门":
			# 不创建提货单,直接创建已入库的托运单
			ruKuResult = new_YiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId,
									   sendStationName, receiveStationId, receiveStationName, goodsName)
			if ruKuResult['status'] == 200:
				tydbId = mysql.getTydbId(ruKuResult['tydId'])
				# 创建分拨单
				createFenBoDanResult = createFenBoDan.createFenBoDan(merchantToken,fbdToken, fbdId, tydbId, createrName, createrId, fbdRollOutPointId,
											fbdRollOutPoint,fbdRollInPointId, fbdRollInPoint)
				if createFenBoDanResult['status'] == 200:
					# 创建配载单
					createPeiZaiDanResult = createPeiZaiDan.createPeiZaiDan(merchantToken, pzdId, tydbId, createrName,
																			createrId, pzdRollOutId,pzdRollOutPoint, pzdRollInPointId,pzdRollInPoint)
					if createPeiZaiDanResult['status'] == 200:
						peiZaiResult['status'] = createPeiZaiDanResult['status']
						peiZaiResult['message'] = createPeiZaiDanResult['message']
						peiZaiResult['tydId'] = ruKuResult['tydId']
						print("创建分拨单，不创建提货单，已配载状态的托运单创建成功")
					else:
						peiZaiResult['status'] = createPeiZaiDanResult['status']
						peiZaiResult['message'] = createPeiZaiDanResult['message']
						print("创建分拨单，不创建提货单，已配载状态的托运单创建失败")
				else:
					peiZaiResult['status'] = createFenBoDanResult['status']
					peiZaiResult['message'] = createFenBoDanResult['message']
					print("分拨单创建失败，已配载状态的托运单创建失败")
			else:
				peiZaiResult['status'] = ruKuResult['status']
				peiZaiResult['message'] = ruKuResult['message']
				print("托运单创建失败，已配载状态的托运单创建失败")

		else:
			# 创建提货单,再创建已入库的托运单
			ruKuResult = yiRuKu.yiruku(merchantToken, createrName, createrId, pickGoodsWay, sendStationId, sendStationName,
								   receiveStationId, receiveStationName, goodsName, thdId, takeGoodsStation, takeGoodsStationId)
			#print "ruKuResult:%s"
			if ruKuResult['status'] == 200:
				tydbId = mysql.getTydbId(ruKuResult['tydId'])
				# 创建分拨单
				createFenBoDanResult = createFenBoDan.createFenBoDan(merchantToken, fbdToken, fbdId, tydbId, createrName, createrId, fbdRollOutPointId,
												fbdRollOutPoint, fbdRollInPointId, fbdRollInPoint)
				if createFenBoDanResult['status'] == 200:
					# 创建配载单
					createPeiZaiDanResult = createPeiZaiDan.createPeiZaiDan(merchantToken, pzdId, tydbId, createrName,
																			createrId, pzdRollOutId, pzdRollOutPoint,
																			pzdRollInPointId, pzdRollInPoint)
					if createPeiZaiDanResult['status'] == 200:
						peiZaiResult['status'] = createPeiZaiDanResult['status']
						peiZaiResult['message'] = createPeiZaiDanResult['message']
						peiZaiResult['tydId'] = ruKuResult['tydId']
						print("创建分拨单，要创建提货单，已配载状态的托运单创建成功")
					else:
						peiZaiResult['status'] = createPeiZaiDanResult['status']
						peiZaiResult['message'] = createPeiZaiDanResult['message']
						print("创建分拨单，要创建提货单，已配载状态的托运单创建失败")
				else:
					peiZaiResult['status'] = createFenBoDanResult['status']
					peiZaiResult['message'] = createFenBoDanResult['message']
					print("分拨单创建失败，已配载状态的托运单创建失败")
			else:
				peiZaiResult['status'] = ruKuResult['status']
				peiZaiResult['message'] = ruKuResult['message']
				print("托运单创建失败，已配载状态的托运单创建失败")

	return peiZaiResult





