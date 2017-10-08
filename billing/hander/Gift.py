# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.dao.giftDao import GiftDao
from billing.db.object.models import Gift
from billing.db.object.models import Order
from billing.util.handlerUtil import *
from billing.hander.Recharge import generation
import json
from oslo_log import log as logging
import traceback
LOG = logging.getLogger(__name__)

def giftAmount(account_id, giftJson, headers=None, **kwargs):
    try:
        if isinstance(giftJson, str):
            giftJson = json.loads(giftJson)
        LOG.info('rechargeJson ..'+json.dumps(giftJson))
        print giftJson
        giftDict = giftJson['gift']
        gift = Gift()
        getObjFromJson(gift, giftDict)
        order = Order()
        order.account_id = account_id
        order.amount = gift.amount
        order.payment_type = "gift" #"recharge" "gift"
        order.status = "pay_success"  # "ardered","pay_success","pay_error"
        order.order_no = generation()
        gift.order=order
        giftDao = GiftDao(gift)
        giftDao.giftAmount(account_id)
        return outSuccess("gift", getJsonFromObj(giftDao.gift))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("生成赠送金额失败！")

def firstAmount(account_id,giftJson,headers=None,**kwargs):
    '''
    判断是否是第一次充值，如果是则进行充值，如果不是，返回false
    :param account_id:
    :param giftJson:
    :param headers:
    :param kwargs:
    :return:
    '''
    try:
        if isinstance(giftJson,str):
            giftJson = json.loads(giftJson)
        LOG.info('firstGift..'+json.dumps(giftJson))
        print giftJson
        giftDict = giftJson['gift']
        gift = Gift()
        getObjFromJson(gift, giftDict)
        order = Order()
        order.account_id = account_id
        order.amount = gift.amount
        order.payment_type = "gift" #"recharge" "gift"
        order.status = "pay_success"  # "ardered","pay_success","pay_error"
        order.order_no = generation()
        gift.order=order
        giftDao = GiftDao(gift)
        if giftDao.isFirstGift(account_id):
            giftDao.giftAmount(account_id)
            return outSuccess("gift", getJsonFromObj(giftDao.gift))
        else:
            return outError("首次赠送金额失败！")
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("首次赠送金额失败！")

if __name__=="__main__":
    import datetime
    giftJson={"gift":{"gift_by":"xiaow","status":"pay_success","gift_at":"2015-09-10 16:03:58","amount":1234.00}}
    giftAmount("asdasjdjajsdjsajdj",giftJson)

