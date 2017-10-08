# -*- coding:utf-8 -*-
'''
Created on 2015年9月10日

@author: greshem
'''
from billing.api import wsgi
from billing.hander import Recharge
from billing.hander.Recharge import getinsteadrechargelist
from billing.util.controllerUtil import *
import json
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC

class Controller(wsgi.Controller):
    
    def create(self,req, **args):
        '''生成充值'''
        account_id=args.get('account_id')
        return Recharge.create(account_id,json.dumps(req.json_body))
    
    def getOrderRechargeList(self,req, **args):
        page_no = req.params.get('pageNo')
        page_size = req.params.get('pageSize')
        page_no = int(page_no) if page_no else 1
        page_size = int(page_size) if page_size else 15
        account_id = args.get('account_id')
        payment_type=req.params.get('payment_type')
        started_at=req.params.get('started_at')
        started_at=change2UTC(started_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        ended_at=req.params.get('ended_at')
        ended_at=change2UTC(ended_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        return Recharge.getOrderRechargeList(account_id, payment_type, started_at, ended_at,page_no,page_size)

    def insteadRecharge(self, req, **args):
        '''代充值'''
        return Recharge.insteadRecharge(json.dumps(req.json_body))
    # added by zhangaw
    def getInsteadRecharge(self,req,**args):
        '''获取代充值列表'''
        instead_recharge_account=args.get('instead_recharge_account')
        conditiondict=getDictFromReq(req)
        return Recharge.getinsteadrechargelist(instead_recharge_account,conditiondict)

    def getInsteadAmount(self,req,**args):
        '''获取代充值总额'''
        instead_account=args.get('instead_recharge_account')
        return Recharge.getinsteadamount(instead_account,**args)
    # end edit

def create_resource():
    return wsgi.Resource(Controller())