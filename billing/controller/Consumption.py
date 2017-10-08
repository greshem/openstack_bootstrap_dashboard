# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from oslo_utils import strutils
import webob

from billing.api import wsgi
from billing import exception
from billing.i18n import _
from billing import utils
from billing.hander import Consumption
import datetime
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC

class Controller(wsgi.Controller):
    """消费记录"""
    def list(self,req,**args):
        page_no = req.params.get('pageNo')
        page_size = req.params.get('pageSize')
        page_no = int(page_no) if page_no else 1
        page_size = int(page_size) if page_size else 15
        account_id = args.get('account_id')
        started_at = req.params.get('started_at')
        if started_at is None:
            started_at=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m')+'-01'
        started_at=change2UTC(started_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        ended_at = req.params.get('ended_at')
        if ended_at is None:
            ended_at=datetime.datetime.utcnow()
        else:
            ended_at=change2UTC(ended_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        region_id=req.params.get('region_id')
        resource_type=req.params.get('resource_type')
        return Consumption.consumptionList(account_id, started_at, ended_at,region_id,resource_type,page_no,page_size)
    
    def forecast(self,req,**args):
        '''消费预测'''
        account_id = args.get('account_id')
        return Consumption.consumptionForecast(account_id)
    
    def getAmountSummary(self,req,**args):
        '''账户消费总额汇总'''
        account_id = args.get('account_id')
        started_at = req.params.get('started_at')
        if started_at is None:
            started_at=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m')+'-01'
        started_at=change2UTC(started_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        ended_at = req.params.get('ended_at')
        if ended_at is None:
            ended_at=datetime.datetime.utcnow()
        else:
            ended_at=change2UTC(ended_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        return Consumption.getAmountSummary(account_id, started_at, ended_at)
    
    def getConsumptionSummary(self,req,**args):
        '''账户消费明细汇总'''
        account_id = args.get('account_id')
        started_at = req.params.get('started_at')
        if started_at is None:
            started_at=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m')+'-01'
        started_at=change2UTC(started_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        ended_at = req.params.get('ended_at')
        if ended_at is None:
            ended_at=datetime.datetime.utcnow()
        else:
            ended_at=change2UTC(ended_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        return Consumption.getConsumptionSummary(account_id, started_at, ended_at)

def create_resource():
    return wsgi.Resource(Controller())