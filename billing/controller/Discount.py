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
from billing.hander import Discount
from billing.util.controllerUtil import *
import json

class Controller(wsgi.Controller):
    """折扣管理"""
    def create(self, req, **args):
        jsonParams = req.json_body
        account_id = args.get('account_id')
        jsonParams['discount']['account_id'] = account_id
        return Discount.add(json.dumps(jsonParams))
    
    def update(self, req, **args):
        jsonParams = req.json_body
        account_id = args.get('account_id')
        jsonParams['discount']['account_id'] = account_id
        return Discount.update(json.dumps(jsonParams))
    
    def list(self, req, **args):
        account_id = args.get('account_id')
        region_id = req.params.get('region_id')
        return Discount.getDiscountList(account_id, region_id)
    
    def detail(self, req, **args):
        account_id = args.get('account_id')
        conditionJson = getDictFromReq(req, inKeys=('billing_item_id', 'region_id', 'billing_item'))
        if account_id:
            conditionJson['account_id'] = account_id
        return Discount.getDiscountDetail(json.dumps(conditionJson))


def create_resource():
    return wsgi.Resource(Controller())
