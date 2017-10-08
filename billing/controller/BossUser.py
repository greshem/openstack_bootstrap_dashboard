# -*- coding:utf-8 -*-
'''
Created on 2015-12-18

@author: yamin
Boss系统的用户数据库操作类
'''
from billing.api import wsgi
from oslo_config import cfg
CONF = cfg.CONF
from billing.db.dao import bossuserDao
from billing.util.handlerUtil import *
from oslo_log import log as logging
import traceback
LOG = logging.getLogger(__name__)
not_include=["records","type",]

class Controller(wsgi.Controller):
    def saler_list(self,req,*args,**kwargs):
        try:
            record=bossuserDao.BossUserDao().sale_list()
            return outSuccess("boss_sale_user", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("获取销售人员列表失败！")

def create_resource():
    return wsgi.Resource(Controller())