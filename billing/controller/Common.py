# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from oslo_utils import strutils
import webob

from billing.api import wsgi
from billing.hander import Common

class Controller(wsgi.Controller):
    """公共接口"""
    def getRegionList(self,req,**args):
        return Common.getRegionList()
    
    def checkProjectAdmin(self,req,**args):
        account_id = args.get('account_id')
        return Common.checkProjectAdmin(account_id)
    
def create_resource():
    return wsgi.Resource(Controller())