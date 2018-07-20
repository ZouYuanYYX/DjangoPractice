# -*- coding:utf-8 -*-
# author 邹元
import sys
from merchant import createPeiSongDan
from merchant import yiPeiSongWaitTransport
reload(sys)
sys.setdefaultencoding('utf8')

#已配送-待运输
#创建运输中状态的托运单，先创建托运单，再创建提货、分拨、配载单等，需要对配载单做发车动作
#pzdRollInPoint:配载单转入网点
#pzdRollOutPoint:配载单转出网点

def yiPeiSongTransporting(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken,psdId,deliveryPoint) :

	# 定义接口的返回值
	yiPeiSongTransportingResult = {"status": 0, "message": '', "tydId": ''}
	#创建已配送状态的托运单
	yiPeiSongWaitTransportResult = yiPeiSongWaitTransport.yiPeiSongWaitTransport(merchantToken,generateFenBoDan,createrName,createrId,pickGoodsWay,sendStationId,
			 sendStationName,receiveStationId,receiveStationName,goodsName,thdId,takeGoodsStation,takeGoodsStationId,
			 pzdRollOutPoint,pzdRollInPoint,pzdId,fbdId,fbdRollOutPoint,fbdRollInPoint,fbdToken,pzdToken,psdId,deliveryPoint)

	if yiPeiSongWaitTransportResult['status'] == 200:
		# 配送单配送,pzdToken可以直接传配载单用户的token，因为配载单转入网点与配送网点相同，
		# 有转入网点的权限，就肯定有配送网点的权限
		peiSongResult = createPeiSongDan.peiSong(merchantToken, psdId, pzdToken)
		if peiSongResult['status'] == 200:
			yiPeiSongTransportingResult['status'] = peiSongResult['status']
			yiPeiSongTransportingResult['message'] = peiSongResult['message']
			yiPeiSongTransportingResult['tydId'] = yiPeiSongWaitTransportResult['tydId']
			print("已配送状态的托运单创建成功（配送单运输中）")
		else:
			yiPeiSongTransportingResult['status'] = peiSongResult['status']
			yiPeiSongTransportingResult['message'] = peiSongResult['message']
			print("配送单配送失败！")
	else:
		yiPeiSongTransportingResult['status'] = yiPeiSongWaitTransportResult['status']
		yiPeiSongTransportingResult['message'] = yiPeiSongWaitTransportResult['message']
		print("已配送状态的托运单创建失败（配送单运输中）")
	return yiPeiSongTransportingResult


