# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from billing.db.dao.discountDao import DiscountDao 
from billing.db.object.models import Discount
from billing.util.handlerUtil import *
from oslo_log import log as logging
from billing.util.pagePackage import *
import traceback

LOG = logging.getLogger(__name__)
DISCOUNT_OBJECT_KEY = ['billing_item']

def add(discountJson, headers=None, **kwargs):
    try:
        if isinstance(discountJson,str):
            discountJson = json.loads(discountJson)
        discountDict = discountJson['discount']
        if not checkDiscount(discountDict):
            return outError("该折扣已经存在！")
        discount = Discount()
        getObjFromJson(discount, discountDict)
        discountDao = DiscountDao(discount)
        discountDao.add()
        return outSuccess("discount", getJsonFromObj(discountDao.discount))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("创建折扣失败！")

def checkDiscount(discountJson):
    try:
        discountDao = DiscountDao()
        result=discountDao.getDiscountByCondition(discountJson)
        return False if result else True
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        raise e

def update(discountJson, headers=None, **kwargs):
    try:
        if isinstance(discountJson,str):
            discountJson = json.loads(discountJson)
        discountDict = discountJson['discount']
        discount = Discount()
        discount.discount_id=discountDict['discount_id']
        discountDao = DiscountDao(discount)
        discountDao.update(discountDict)
        return outSuccess("discount", getJsonFromObj(discountDao.discount))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新折扣失败！")

def getDiscountDetail(discountJson): 
    try:
        discountJson = json.loads(discountJson)
        discountDao = DiscountDao()
        return outSuccess("discount", getJsonFromObj(discountDao.getDiscountDetail(discountJson)))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得折扣失败！")  

def getDiscountList(account_id,region_id=None):
    try:
        discountDao = DiscountDao()
        result=discountDao.list(account_id,region_id)
        dataResult = []
        if result:
            for account in result:
                dataResult.append(getJsonFromObj(account))
        return outSuccess("discountList", dataResult)
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得折扣列表失败！")  


if __name__=='__main__':
#    discountJson='{"discount":{"discount_id":32,"account_id":"szfdsfdsfgdfg","billing_item_id":4,"discount_ratio":0.55}}'
    discountJson='{"region_id":"region1","account_id":"szfdsfdsfgdfg","billing_item":"instance_1"}'
    print getDiscountDetail(discountJson)
