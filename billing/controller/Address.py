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
from billing.hander import Address
import json

class Controller(wsgi.Controller):
    """地址管理"""
    def list(self,req,**args):
        account_id=args.get('account_id')
        return Address.list(account_id)
    
    def create(self,req,**args):
        account_id=args.get('account_id')
        jsonParams = req.json_body
        jsonParams['address']['account_id']=account_id
        return Address.add(json.dumps(jsonParams))
    
    def update(self,req,**args):
        jsonParams = req.json_body
        return Address.update(jsonParams)
    
    def delete(self,req,**args):
        address_id=args.get('address_id')
        return Address.delete(address_id)

def create_resource():
    return wsgi.Resource(Controller())