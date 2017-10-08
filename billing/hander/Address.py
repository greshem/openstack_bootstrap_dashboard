# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from billing.db.dao.addressDao import AddressDao
from billing.db.object.models import Address
from billing.util.handlerUtil import *
from oslo_log import log as logging
import traceback

LOG = logging.getLogger(__name__)

ADDRESS_OBJECT_KEY=['account']

def list(account_id):
    try:
        addressDao=AddressDao()
        result=addressDao.list(account_id)
        dataResult=[]
        if result:
            dataResult=[getJsonFromObj(address,ADDRESS_OBJECT_KEY) for address in result]
        return outSuccess("addresses",dataResult)
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得地址列表失败！")

def add(addressJson,headers=None, **kwargs):
    try:
        if isinstance(addressJson, str):
            addressJson = json.loads(addressJson)
        addressDict = addressJson['address']
        address = Address()
        getObjFromJson(address, addressDict)
        addressDao = AddressDao(address)
        addressDao.add()
        return outSuccess("account", getJsonFromObj(addressDao.address))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("创建地址失败！")



def update(addressJson,headers=None,**kwargs):
    try:
        if isinstance(addressJson, str):
            addressJson = json.loads(addressJson)
        addressDict = addressJson['address']
        address = Address()
        getObjFromJson(address, addressDict)
        addressDao = AddressDao(address)
        addressDao.update(addressDict)
        return outSuccess("account", getJsonFromObj(addressDao.address))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新地址失败！")

def delete(address_id,headers=None,**kwargs):
    try:
        address = Address()
        address.address_id=address_id
        addressDao = AddressDao(address)
        addressDao.update({"status":"deleted"})
        return outSuccess("msg", "删除账户成功！")
    except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("删除地址失败！")
    
def detail(address_id,headers=None,**kwargs):
    try:
        address = Address()
        address.address_id=address_id
        addressDao = AddressDao(address)
        addressDao.detail()
        return outSuccess("account", getJsonFromObj(addressDao.address))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得地址失败！")

    
if __name__=='__main__':
    addressJson='{"address":{"account_id":"szfdsfdsfgdfg","name":"bao234","address_id":6}}'
    print detail(6)

    