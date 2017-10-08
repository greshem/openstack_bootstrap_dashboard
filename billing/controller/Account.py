# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from oslo_utils import strutils
import webob

from billing.api import wsgi
from billing.hander import Account
from billing.util.controllerUtil import *

import json 
import datetime
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC

class Controller(wsgi.Controller):
    """账户接口处理"""
    def list(self, req, **args):
        page_no = req.params.get('pageNo')
        page_size = req.params.get('pageSize')
        page_no = int(page_no) if page_no else 1
        page_size = int(page_size) if page_size else 15
        conditionJson = getDictFromReq(req, inKeys=('type', 'status'))
        likeConditionjson = getDictFromReq(req, inKeys=('username'))
        return Account.listByPage(json.dumps(conditionJson), json.dumps(likeConditionjson), page_no, page_size)
    
    def create(self, req, **args):
        jsonParams = req.json_body
        return Account.add(jsonParams)
    
    def update(self, req, **args):
        account_id = args.get('account_id')
        jsonParams = req.json_body
        jsonParams['account']['account_id'] = account_id
        return Account.update(json.dumps(jsonParams))
    
    def delete(self, req, **args):
        account_id = args.get('account_id')
        return Account.delete(account_id)
    
    def detail(self, req, **args):
        account_id = args.get('account_id')
        return Account.detail(account_id)
    
    def changeCreditLine(self, req, **args):
        account_id = args.get('account_id')
        credit_line=req.params.get('credit_line')
        return Account.changeCreditLine(account_id,credit_line)
    
    def change2Credit(self, req, **args):
        account_id = args.get('account_id')
        credit_line=req.params.get('credit_line')
        return Account.change2Credit(account_id,credit_line)

    def detail_dict(self,req,**args):
        account_id = args.get('account_id')
        return Account.detail_dict(account_id)

    def getAccountByUserID(self, req, **args):
        user_id = args.get('user_id')
        return Account.getAccountByUserID(user_id)
    
    def getAccountByProjectId(self, req, **args):
        project_id = args.get('tenant_id')
        return Account.getAccountByProjectId(project_id)
    
    def getSubAccountSum(self, req, **args):
        account_id = args.get('account_id')
        return Account.getSubAccountSum(account_id)
    
    def subAccountList(self, req, **args):
        page_no = req.params.get('pageNo')
        page_size = req.params.get('pageSize')
        page_no = int(page_no) if page_no else 1
        page_size = int(page_size) if page_size else 15
        account_id = args.get('account_id')
        conditionJson = getDictFromReq(req, inKeys=('type', 'name', 'max_cash', 'min_cash', 'max_gift', 'min_gift', 'max_credit', 'min_credit'))
        return Account.subAccountList(account_id, conditionJson, page_no, page_size)

    def getProAdmSubAccount(self,req,**args):
        account_id = args.get('account_id')
        condition=getDictFromReq(req)
        return Account.ProjectAdminsubAccountList(account_id, condition=condition)


    def subAccountDetail(self, req, **args):
        account_id = args.get('account_id')
        return Account.subAccountDetail(account_id)
    
    def subAccountAmountSum(self, req, **args):
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
        return Account.subAccountAmountSum(account_id,started_at,ended_at)
    
    def subAccountConsumptionList(self,req, **args):
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
        conditionJson = getDictFromReq(req, inKeys=('type', 'name'))
        return Account.subAccountConsumptionList(account_id,started_at,ended_at,conditionJson,page_no,page_size)
    
    def checkAdmin(self,req,**args):
        account_id = args.get('account_id')
        return Account.checkAdmin(account_id)
    
    def lowCashWorkOrder_3(self,req,**args):
        return Account.lowcashReminder_3()
    
    def getParentUserById(self, req, **args):
        user_id = args.get('user_id')
        return Account.getParentUserByID(user_id)
    
#    def getAccountByUserMD5(self, req, **args):
#        user_md5=args.get('user_md5')
#        return Account.getAccountByUserMD5(user_md5)


def create_resource():
    return wsgi.Resource(Controller())
