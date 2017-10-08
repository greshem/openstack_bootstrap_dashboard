# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.dao.alipayInfoDao import AlipayInfoDao
from billing.db.object.models import AlipayInfo
import json
from oslo_log import log as logging
from billing.util.handlerUtil import *
import traceback

LOG = logging.getLogger(__name__)

def rechargeAmount(alipayInfoJson, headers=None, **kwargs):
    """充值金额"""
    try:
        if isinstance(alipayInfoJson, str):
            alipayInfoJson = json.loads(alipayInfoJson)
        LOG.info('alipayInfoJson ..'+json.dumps(alipayInfoJson))
        alipayInfoDict = alipayInfoJson['alipayInfo']
        alipayInfo = AlipayInfo()
        getObjFromJson(alipayInfo, alipayInfoDict)
        LOG.info('rechargeAmount  start..'+json.dumps(alipayInfoJson))
        alipayInfoDao = AlipayInfoDao(alipayInfo)
#        LOG.info('rechargeAmount  start..'+json.dumps(getJsonFromObj(alipayInfoJson)))
        result = alipayInfoDao.rechargeAmount()
#        LOG.info('rechargeAmount  end..'+json.dumps(getJsonFromObj(alipayInfoDao.alipayInfo)))
        if result:
            return outSuccess("msg", result)
        return outSuccess("alipayInfo", getJsonFromObj(alipayInfoDao.alipayInfo))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("创建账户失败！")



if __name__=='__main__':
    alipayInfoJson={"alipayInfo":{"order_no":100000002,"status":"pay_error","trade_no":"123456786","pay_at":"2015-09-10 15:09:50","amount":2000.00}}
    print rechargeAmount(alipayInfoJson)


