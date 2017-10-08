# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.dao.cdnDomainDao import cdnDomainDao
# from billing.db.object.models import CDNDomain

from billing.util.handlerUtil import *
import json
from oslo_log import log as logging
from billing.util.pagePackage import *
import traceback

LOG = logging.getLogger(__name__)


def create(tenant_id, cdndomainJson, headers=None, **kwargs):
    """创建CDN信息"""
    try:
        pass
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("生成CDN记录失败！")

def getCDNDomainList(tenant_id=None):
    try:
        CDNDomainDao = cdnDomainDao()
        result = CDNDomainDao.getCDNDomainList(tenant_id)
        # dataResult=[]
        # if result:
        #     dataResult=[getJsonFromObj(item) for item in result]
        return outSuccess("cdn_domains", result)

    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得CDN列表失败！")

def updateCdnDomainEnable(domain_id,enable,status):
    try:
        CDNDomainDao = cdnDomainDao()
        CDNDomainDao.updateCdnDomainEnable(domain_id, enable,status)
        # dataResult=[]
        # if result:
        #     dataResult=[getJsonFromObj(item) for item in result]
        return outSuccess("msg", "更新Enable状态成功！")

    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新enable失败！")

