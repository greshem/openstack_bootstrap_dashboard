# -*- coding:utf-8 -*-
'''
Created on 2015-12-18

@author: yamin
账户数据库操作类
'''
from billing.api import wsgi
from billing.hander import WorkOrder
from billing.hander.Recharge import getinsteadrechargelist
from billing.util.controllerUtil import *
import json
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC
from billing.db.dao.actionLogDao import *
#from billing.util.handlerUtil import *
import traceback
from sqlalchemy import desc
class Controller(wsgi.Controller):
    def insert_log(self,req,*args,**kwargs):
        '''
        插入一条记录
        :return:
        '''
        try:
            log_dict=req.json_body
            ActionLogDao().insert_log(log_dict)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("插入日志信息失败！")

    def actionlog_list(self,req,*args,**kwargs):
        """
        :return:
        """
        try:
            info={
                "condition":{
                    "dateFrom":req.params.get('dateFrom'),
                    "dateTo":req.params.get('dateTo'),
                    "keyword":"%"+req.params.get('keyword')+"%" if req.params.get('keyword') else None,
                },
                "page":{
                    "offset":req.params.get('offset'),
                    "page_size":req.params.get('pageSize')
                }
            }
            records,total=ActionLogDao().list(info)
            return json.dumps({"logs":records,"total":total,"success":"success"},cls=CJsonEncoder, ensure_ascii=False)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("获取日志失败！")

def create_resource():
    return wsgi.Resource(Controller())