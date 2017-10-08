# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from billing.util.handlerUtil import *
from oslo_log import log as logging
from billing.db.dao.commonDao import CommonDao
from billing.db.dao.accountDao import AccountDao
from billing.db.object.models import Account
import traceback

LOG = logging.getLogger(__name__)

def getRegionList():
    '''得到区域列表'''
    try:
        commonDao = CommonDao()
        return outSuccess('regionList', commonDao.getRegionList())
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("服务器错误")

def checkProjectAdmin(account_id):
    '''判断是否是分销商用户'''
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail()
        commonDao = CommonDao()
        return outSuccess('isProjectAdmin', commonDao.checkProjectAdmin(accountDao.account.user_id))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("服务器错误")
