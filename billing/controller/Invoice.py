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
from billing.hander import Invoice
from billing.util.controllerUtil import *
import json

class Controller(wsgi.Controller):
    """发票管理"""
    def create(self, req, **args):
        jsonParams = req.json_body
        account_id = args.get('account_id')
        jsonParams['invoice']['account_id']=account_id
        return Invoice.add(json.dumps(jsonParams))
    
    def update(self, req, **args):
        jsonParams = req.json_body
        account_id = args.get('account_id')
        jsonParams['invoice']['account_id']=account_id
        return Invoice.update(json.dumps(jsonParams))
    
    def list(self, req, **args):
        account_id = args.get('account_id')
        jsonParams = getDictFromReq(req,inKeys=('type','status'))
        jsonParams['account_id']=account_id
        page_no =req.params.get('page_no')
        page_size = req.params.get('page_size')
        page_no=int(page_no) if page_no else 1
        page_size=int(page_size) if page_size else 15
        return Invoice.listByPage(json.dumps(jsonParams), page_no, page_size)
    
    def detail(self, req, **args):
        invoice_id = args.get('invoice_id')
        return Invoice.detail(invoice_id)

    def summary(self, req, **args):
        account_id = args.get('account_id')
        return Invoice.summary(account_id)




def create_resource():
    return wsgi.Resource(Controller())
