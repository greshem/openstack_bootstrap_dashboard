# -*- coding:utf-8 -*-
'''
Created on 2015-8-26

@author: greshem
'''
from billing.db.dao.billingItemDao import BillingItemDao
from billing.db.object.models import BillingItem
import json
from billing.util.handlerUtil import *
from oslo_log import log as logging
from billing.util.pagePackage import *
import traceback

LOG = logging.getLogger(__name__)

BILLINGITEM_OBJECT_KEY = ["discounts"]

def list(region_id,headers=None, **kwargs):
    '''
        计费项列表
    '''
    try:
        billingItem=BillingItem()
        if region_id:
            billingItem.region_id=region_id
        billingItemDao=BillingItemDao(billingItem)
        result=billingItemDao.list()
        dataResult=[]
        if result:
            for billingItem in result:
                dataResult.append(getJsonFromObj(billingItem,notInDict=BILLINGITEM_OBJECT_KEY))
        return outSuccess("billing_itemList",dataResult)
    except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("取得计费项列表失败！")

def getBillingItem(billing_item_id,region_id,billing_item,headers=None, **kwargs):
    try:
        billingItem=BillingItem()
        if billing_item_id:
            billingItem.billing_item_id=billing_item_id
        if region_id:
            billingItem.region_id=region_id
        if billing_item:
            billingItem.billing_item=billing_item
        billingItemDao=BillingItemDao(billingItem)
        result=billingItemDao.getBillingItem()
        return outSuccess("billing_item",getJsonFromObj(result,BILLINGITEM_OBJECT_KEY))
    except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("取得计费项失败！")

def update(billingItemJson, headers=None, **kwargs):
    try:
        billingItemJson = json.loads(billingItemJson)
        billingItemDict = billingItemJson['billing_item']
        billingItem = BillingItem()
        billingItem.billing_item_id = billingItemDict['billing_item_id']
        billingItemDao=BillingItemDao(billingItem)
        billingItemDao.update(billingItemDict)
        return outSuccess("billing_item", getJsonFromObj(billingItemDao.billingItem, BILLINGITEM_OBJECT_KEY))
    except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("更新计费项失败！")


def get_price_for_nass(network_type, bandwidth, distance):
    try:
        billingItem = BillingItem()
        billingItemDao = BillingItemDao(billingItem)
        result = billingItemDao.get_price_for_nass(network_type, bandwidth, distance)
        return outSuccess("price", result.price * Decimal(bandwidth))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得计费项失败！")

if __name__== '__main__':
#    print getBillingItem(None,'region1','instance_1')
    billingItemJson='{"billing_item":{"billing_item_id":1,"price":100.20}}'
    print update(billingItemJson)
   